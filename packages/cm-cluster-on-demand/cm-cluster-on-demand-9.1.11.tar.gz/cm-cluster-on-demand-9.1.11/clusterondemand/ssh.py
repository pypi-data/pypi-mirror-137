#!/usr/bin/python
# Copyright 2004-2022 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time

import paramiko

from clusterondemand import localpath
from clusterondemand.codoutput.sortingutils import SSHAlias
from clusterondemand.contextmanagers import SmartLock
from clusterondemand.exceptions import CODException
from clusterondemand.utils import (
    is_valid_cluster_name,
    is_valid_ip_address,
    is_valid_positive_integer,
    is_writable_directory
)
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandconfig.configuration_validation import must_be_nonnegative

from .decorators import retry

clusterssh_ns = ConfigNamespace("cluster.ssh")

clusterssh_ns.add_parameter(
    "ssh_identity",
    advanced=True,
    default=None,
    help="Path to an ssh identity file key. Multiple arguments are allowed",
    help_varname="PATH_TO_FILE",
    parser=localpath.localpath,
    validation=[localpath.must_exist, localpath.must_be_readable]
)

clusterssh_ns.add_parameter(
    "ssh_password",
    advanced=True,
    default=None,
    help="SSH password to access the cluster",
    secret=True,
)

clusterssh_ns.add_parameter(
    "ssh_connect_timeout",
    advanced=True,
    default=30,
    help="Timeout for establishing an SSH connection with the cluster",
    validation=must_be_nonnegative,
)

log = logging.getLogger("cluster-on-demand")

# Suppress paramiko's logging
logging.getLogger("paramiko").setLevel(logging.WARNING)


class SSHConfigManagerException(Exception):
    """SSH configuration manager specific exceptions base class."""
    pass


class MultipleCodTypesException(Exception):
    """"""
    pass


# ssh directives (cf. man ssh_config)
HOST_ = "Host "
HOSTNAME_ = "HostName "


class SSHConfigHostDescriptor(object):
    """
    :param host: the host name, must be a valid cluster name.
    :param index: the index used to build the alias.
    :param prefix: the prefix used to build the alias.
    :param ip: the host IP, must be a valid IPv4 address.
    """
    # Notice: this ctor does not perform any validation. This is intentional, the instance owner must
    # always check the `is_valid` property to decide whether the instance should be used or discarded.
    def __init__(self, host, index, prefix, ip):
        self._host = host
        self._index = index
        self._prefix = prefix
        self._ip = ip

    @property
    def is_valid(self):
        return (is_valid_cluster_name(self.host) and
                is_valid_ip_address(self.ip) and
                is_valid_positive_integer(self.index))

    @property
    def host(self):
        return self._host

    @property
    def index(self):
        return self._index

    @property
    def ip(self):
        return self._ip

    @property
    def alias(self):
        return "{prefix}{index}".format(
            prefix=self._prefix,
            index=self._index
        )

    @staticmethod
    def from_lines(lines, prefix):
        host, index, ip = (None, ) * 3
        try:
            for line in (l.strip() for l in lines):
                if line.startswith(HOST_):
                    line = line.replace(HOST_, "").strip()

                    tmp = line.split(" ")
                    host = tmp[0]
                    index = int(tmp[1].replace(prefix, ""))

                elif line.startswith(HOSTNAME_):
                    line = line.replace(HOSTNAME_, "").strip()
                    ip = line.split(" ")[0]
        except Exception:
            pass  # silence errors

        return SSHConfigHostDescriptor(host, index, prefix, ip)

    def __str__(self):
        return textwrap.dedent("""
        Host {host} {alias}
            HostName {ip}
            User root
            UserKnownHostsFile /dev/null
            StrictHostKeyChecking=no
            CheckHostIP=no
            LogLevel=error""".format(host=self.host, alias=self.alias, ip=self.ip))


class SSHConfigManager(object):
    """
    A helper class to manage cluster-related entries in local ssh_config file.

    :param cod_type: the type of cod clusters to be managed, i.e os or vmware.
    :param ssh_config: the path of the local ssh configuration file to use.
    :param prefix: the prefix used to build the cluster ssh aliases.
    :param parse: enable parsing the contents of the ssh_config file.
    :param mode: Either "match-hosts" or "replace-hosts". "match-hosts" preserves the contents of the
                 COD section or the ssh_config file; "replace-hosts" ignores currently defined hosts.
                 User-defined contents are always preserved.
    """
    def __init__(self, cod_type, ssh_config="~/.ssh/config", prefix="", parse=True, mode="match-hosts"):

        # params
        self._ssh_config = os.path.expanduser(ssh_config)
        self._prefix = prefix
        if mode not in ["match-hosts", "replace-hosts"]:
            raise SSHConfigManagerException("Programming error")
        self._mode = mode

        # internals
        self._begin_marker = f"#### BEGIN COD-{cod_type.upper()} SECTION"
        self._end_marker = f"#### END COD-{cod_type.upper()} SECTION"
        self._cod_type = cod_type
        self._hosts = []
        self._cod_section = []
        self._usr_section = []

        self._parsed = False
        self._changed = False

        # disabling parsing of the local ssh config can be useful if the configuration is actually broken
        if parse:
            if not os.path.exists(self._ssh_config):
                # Non-existing config file is equivalent to empty config file
                log.warning("File '%s' was not found, continuing with an empty configuration.",
                            self._ssh_config)
                self._parsed = True
            else:
                try:
                    with open(self._ssh_config, "r") as config:
                        self._parse_config(config)
                        self._parsed = True

                except IOError as ioe:
                    log.warning(str(ioe))

    @staticmethod
    def lock(ssh_config="~/.ssh/config"):
        return SmartLock(os.path.expanduser(ssh_config) + ".lock")

    def _check_parsed(self):
        if not self._parsed:
            raise SSHConfigManagerException(
                "File '%s' not successfully parsed",
                self._ssh_config
            )

    @property
    def hosts(self):
        """A list of host descriptors"""
        self._check_parsed()
        return self._hosts

    @property
    def user(self):
        """Contents of the user section"""
        self._check_parsed()
        return self._usr_section

    def add_host(self, host, ip, override=False):
        """
        Add a host descriptor to current configuration. Invalid descriptors are discarded.

        :param host: the hostname (string)
        :param ip: the host IPv4 or IPv6 address (string)
        :param override: (reserved for cluster create) if another host with the same name already exists, remove the
        the corresponding entry before adding this host. If override is False, trying to add an already existing host
        will raise an exception.

        :return: the host descriptor that has been added.
        """
        self._check_parsed()

        exists = next((h for h in self._hosts if h.host == host), None)
        if exists:
            if override:
                log.warning("Replacing local ssh config entry for host '%s'", host)
                self.remove_host(host)
            else:
                raise SSHConfigManagerException("A descriptor already exists for host '%s'" % host)

        next_index = max((h.index for h in self._hosts)) + 1 if self._hosts else 1

        res = SSHConfigHostDescriptor(host, next_index, self._prefix, ip)
        self._safe_add_host_descriptor(res)

        return res

    def remove_host(self, host):
        """
        Remove a host descriptor from current configuration

        :param host: the hostname (string)
        """
        self._check_parsed()
        prev_hosts = self._hosts
        self._hosts = [h for h in prev_hosts if h.host != host]
        if self._hosts != prev_hosts:
            self._changed = True
        else:
            log.debug(
                "host descriptor for '%s' could not be found.", host)

    def write_configuration(self):
        """
        Write configuration to ssh config file.

        SSH clients give higher priority to entries towards the top of the config
        files. Therefore the COD section is put at the head of the local ssh config
        file. If no hosts are defined (i.e. no clusters), the section will be omitted.
        """
        msg = "cowardly refusing to write file '{ssh_config}'!".format(
            ssh_config=self._ssh_config
        )

        if not self._parsed:
            log.debug("%s (file was not parsed).", msg)
            return

        if not self._changed:
            log.debug("%s (no changes detected).", msg)
            return

        if not is_writable_directory(os.path.dirname(self._ssh_config)):
            log.debug("%s (directory is not writable).", msg)
            return

        assert self._parsed and self._changed
        log.debug("rewriting local ssh config file '%s' with %d COD %s.",
                  self._ssh_config, len(self._hosts),
                  "entry" if 1 == len(self._hosts) else "entries")

        try:
            # we go the extra mile of writing the new config to a temp file and only when we known
            # everything went smooth, we overwrite the pre-existing file by copying the new one onto it.

            with tempfile.NamedTemporaryFile(mode="wt") as fd:
                # Write COD section
                if self._hosts:
                    fd.write(self._begin_marker)
                    fd.write(textwrap.dedent(f"""
                    #### NOTICE: This section of the file is managed by cm-cod-{self._cod_type}. Manual changes to this section will be
                    #### overwritten next time cm-cod-{self._cod_type} cluster create, delete or list --update-ssh-config is executed."""))  # noqa

                    for descr in self._hosts:
                        # no point in keeping invalid entries here
                        if not descr.is_valid:
                            log.debug("Skipping invalid host descriptor for '%s'",
                                      descr.host or "?")
                            continue

                        fd.write(str(descr))
                        fd.write("\n")

                    fd.write(self._end_marker)
                    fd.write("\n")

                # Dump non-COD config as-is
                for line in self._usr_section:
                    fd.write(line)
                fd.flush()

                shutil.copy(fd.name, self._ssh_config)

                # issue warning if preservation of user contents semantics can not be guaranteed: we look for a
                # Host * directive, at the top of the ssh config file. If COD section exists and if this directive
                # can not be found, a warning is issued.
                if self._usr_section and self._hosts:
                    try:
                        if not re.match(r"%s\s+\*" % HOST_.lower().strip(),
                                        next((l for l in (l.strip() for l in self._usr_section if l.strip())
                                              if not l.startswith("#"))).lower()):
                            log.warning(
                                "Possibly unsafe changes were made to '{config}'. To avoid this "
                                "warning, please add a 'Host *' directive right after the end of the "
                                "COD section.".format(
                                    config=self._ssh_config
                                ))
                    except StopIteration:
                        pass

        except IOError as ioe:
            log.warning("Could not write file '%s' (%s).", self._ssh_config, str(ioe))

    def get_host_index(self, host_name):
        try:
            return next(host.index for host in self._hosts if host.host == host_name)
        except StopIteration:
            raise SSHConfigManagerException(f"{host_name} not found in ssh config")

    def get_host_alias(self, host_name):

        try:
            alias_string = next(host.alias for host in self._hosts if host.host == host_name)
            return SSHAlias(alias_string, self._prefix)
        except StopIteration:
            raise SSHConfigManagerException(f"{host_name} not found in ssh config")

    def _safe_add_host_descriptor(self, descriptor):
        """
        If a  valid descriptor is given, add it to the internal cache. Otherwise discard it.

        :param descriptor: An instance of class SSHConfigHostDescriptor
        """
        if descriptor.is_valid:
            self._hosts.append(descriptor)
            self._changed = True
            log.debug("added host descriptor for '%s'", descriptor.host)
        else:
            log.debug("discarding not well-formed descriptor for host '%s'",
                      descriptor.host or "?")

    def _parse_config(self, fd):
        """
        Parse ssh config file.

        :param fd: An open file descriptor

        The ssh config file is logically divided in two sections: the COD section contains
        all host definitions for COD clusters, along with an alias than can be used with ssh
        -like tools, and the IP to reach the head-node and a few configuration options. It is
        enclosed between the begin and end markers; the other section (i.e. anything beyond
        the COD section) is reserved to the user and is preserved as-is.
        """
        if self._mode == "match-hosts":
            self._parse_config_aux(fd)

        elif self._mode == "replace-hosts":
            self._parse_config_aux(fd)
            log.debug("regenerating contents of {config}".format(
                config=self._ssh_config
            ))
            self._hosts = []
            self._changed = True

        else:
            assert False

    def _parse_config_aux(self, fd):
        in_cod_section = False
        for line in fd:
            if line.startswith(self._begin_marker):
                if in_cod_section:
                    raise SSHConfigManagerException(
                        "Unexpected begin marker encountered")
                in_cod_section = True
                continue

            elif line.startswith(self._end_marker):
                if not in_cod_section:
                    raise SSHConfigManagerException(
                        "Unexpected end marker encountered")
                in_cod_section = False
                continue

            elif line.startswith("#### BEGIN") and not self._prefix:
                raise MultipleCodTypesException()

            if in_cod_section and line.startswith("####"):  # skip markers in COD section
                continue

            # every line goes either to the COD section or the user section
            section = self._cod_section if in_cod_section else self._usr_section
            section.append(line)

        # at EOF we're supposed to be out of the COD section
        if in_cod_section:
            raise SSHConfigManagerException(
                "Missing end marker detected")

        # This loop maintains in 'curr' a list of lines. We scan the entire file, line by line, accumulating
        # lines in 'curr'. Every time we encounter a Host declaration we want to process the accumulated lines.
        # Then, we reset the 'curr' list and continue. Once we've scanned the entire file, a few lines will
        # still be in curr. Those will be processed separately.
        curr = []
        for line in self._cod_section:
            # "Match" is not supported within the COD section
            if line.startswith(HOST_):
                if curr:
                    descriptor = SSHConfigHostDescriptor.from_lines(lines=curr, prefix=self._prefix)
                    self._safe_add_host_descriptor(descriptor)
                    curr = []
            curr.append(line)

        # final wrap-up
        if curr:
            descriptor = SSHConfigHostDescriptor.from_lines(lines=curr, prefix=self._prefix)
            self._safe_add_host_descriptor(descriptor)
            curr = []

        assert not curr, "Unexpected"
        log.debug(
            "local ssh config file '%s' parsed, COD section holds %d %s.",
            self._ssh_config, len(self._hosts),
            "entry" if 1 == len(self._hosts) else "entries")


def private_key_for_public(public_key_path):
    if not public_key_path:
        return None

    name, ext = os.path.splitext(public_key_path)
    if os.path.exists(name) and ext:
        return [name]
    else:
        return None


def validate_ssh_access(floating_ip):
    try:
        with SSHExecutor(floating_ip):
            pass
    except SSHAuthenticationError as e:
        raise CODException(textwrap.dedent(f"""
        Authentication error while connecting to root@{floating_ip}. Make sure that provided
        credentials are valid or that you have a valid passwordless SSH access to the cluster.
        Consider using --ssh-identity and/or --ssh-password parameters or using SSH Agent
        with added corresponding identity (recommended).
        If you're creating a cluster check the following options:
        --ssh-key-pair, --ssh-pub-key-path and --ssh-password-authentication.
        """), e)


class SSHExecutorError(Exception):
    pass


class SSHTimeoutError(SSHExecutorError):
    def __init__(self, host, command, stdout, stderr, timeout):
        self.host = host
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.timeout = timeout
        self.message = (f"Command '{self.command}' on the host {self.host} wasn't"
                        f" exited in {self.timeout} seconds")
        super().__init__(self.message)


class SSHAuthenticationError(SSHExecutorError):
    def __init__(self, host):
        self.host = host
        self.message = f"Failed to connect to the host {self.host}: authentication error"
        super().__init__(self.message)


class SSHConnectionError(SSHExecutorError):
    def __init__(self, host):
        self.host = host
        self.message = f"Failed to connect to the host {self.host}: connection error"
        super().__init__(self.message)


class SSHExecutor(object):
    """
    A utility class to interact with a cluster head node via SSH

    :param host: the host (or IP) of the head node
    :param user: the SSH user. If None (default) is used, user `root` will be used
    :param identity_files: the SSH identity files
    :param password: the SSH password
    :param raise_exceptions: If false it returns exit status wherever possible instead of
                             raising exceptions. It's needed for old code only
    :param connect_timeout: number of seconds to retry establishing a connection to the SSH server
    :param wait_between_connect_retries: number of seconds to wait between connection retries
    """

    def __init__(self, host, user=None, identity_files=None, password=None, raise_exceptions=True,
                 connect_timeout=None, wait_between_connect_retries=1):
        if identity_files is None:
            identity_files = config.get("ssh_identity")
        if identity_files is None:
            identity_files = private_key_for_public(config.get("ssh_pub_key_path"))
        if password is None:
            password = config.get("ssh_password")
        if password is None:
            password = config.get("cluster_password")
        if connect_timeout is None:
            connect_timeout = config.get("ssh_connect_timeout")

        # if some command makes use of this class but forgets to import --ssh-connect-timeout,
        # this will lead to unclear errors.
        assert type(connect_timeout) is int and connect_timeout >= 0, "timeout must be positive integer"

        self._host = host
        self._user = user or "root"
        self._identity_files = identity_files
        self._password = password
        self._raise_exceptions = raise_exceptions
        self._keep_connection = False
        self._ssh_client = None
        self._last_error = None
        self._connect_timeout = connect_timeout
        self._wait_between_connect_retries = wait_between_connect_retries

    def __enter__(self):
        self._connect()
        self._keep_connection = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._keep_connection = False
        self._close()

    @property
    def last_error(self):
        """ Get last error raised by ssh client """
        return self._last_error

    def get_ssh_client(self):
        """ Get underlying SSH client. Must be called only inside of the 'with' statement """
        assert self._keep_connection
        return self._ssh_client

    def _close(self):
        if self._ssh_client:
            self._ssh_client.close()
            self._ssh_client = None

    def _try_connect_using_ssh_client(self):
        # This is a small optimization to cache passphrases in SSH Agent and avoid
        # paramiko's bug with asking a passpharse for each private key
        args = [
            "ssh", "-q",
            "-o", "PasswordAuthentication=no",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=1",
            "-o", "BatchMode=yes",  # Avoid stucks because of waiting for keyboard input
            f"{self._user}@{self._host}",
            "exit"
        ]
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as e:
            # This is probably not an error, maybe password auth will work
            # Caller will handle connection/auth errors itself
            log.debug("Authentication using SSH client failed: %s", e)
        else:
            log.debug("Authentication using SSH client was successful")

    def _connect(self):
        if self._ssh_client:
            return

        self._try_connect_using_ssh_client()

        assert self._ssh_client is None
        self._ssh_client = paramiko.SSHClient()
        self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False

        @retry(timeout=self._connect_timeout, wait_between_retries=self._wait_between_connect_retries)
        def connect_wait(time_left, **kwargs):
            log.debug(f"Creating an ssh connection to {self._user}@{self._host} ({time_left:.0f}s left)")
            self._ssh_client.connect(
                self._host,
                username=self._user,
                key_filename=self._identity_files,
                password=self._password,
            )
            log.debug(f"Ssh connection to {self._user}@{self._host} established")

        try:
            connect_wait()
            connected = True
        except paramiko.AuthenticationException as e:
            self._last_error = e
            raise SSHAuthenticationError(self._host) from e
        except Exception as e:
            self._last_error = e
            raise SSHConnectionError(self._host) from e
        finally:
            if not connected:
                self._ssh_client = None

    def run(self, command, timeout=1800, max_stdout_size=100 * 2**20, max_stderr_size=100 * 2**20,
            capture_out=False, capture_err=False):
        if isinstance(command, list):
            command = " ".join(shlex.quote(arg) for arg in command)

        stdin, stdout, stderr, channel = None, None, None, None
        out, err = [], []
        try:
            self._connect()
            stdin, stdout, stderr = self._ssh_client.exec_command(command)
            channel = stdin.channel  # Channel is the same for stdin/stdout/stderr

            # Close write as we don't have any input
            channel.shutdown_write()

            out_size, err_size = 0, 0
            timed_out = False
            end_time = time.monotonic() + timeout
            while time.monotonic() < end_time:
                if channel.recv_ready():
                    if capture_out and out_size < max_stdout_size:
                        chunk = channel.recv(max_stdout_size - out_size)
                        out_size += len(chunk)
                        out.append(chunk)
                    else:
                        chunk = channel.recv(2**20)
                        if not capture_out:
                            sys.stdout.write(chunk.decode("utf-8", errors="replace"))
                        else:
                            pass  # Consume but do nothing to avoid blocking the command
                if channel.recv_stderr_ready():
                    if capture_err and err_size < max_stderr_size:
                        chunk = channel.recv_stderr(max_stderr_size - err_size)
                        err_size += len(chunk)
                        err.append(chunk)
                    else:
                        chunk = channel.recv_stderr(2**20)
                        if not capture_err:
                            sys.stderr.write(chunk.decode("utf-8", errors="replace"))
                        else:
                            pass  # Consume but do nothing to avoid blocking the command
                if channel.closed or channel.exit_status_ready():
                    break
                time.sleep(0.01)
            else:
                timed_out = True

            out = b"".join(out)
            err = b"".join(err)
            status = channel.recv_exit_status() if not timed_out else 255

            if status != 0:
                if status not in range(256):
                    log.debug("recv_exit_status returned unexpected status value: %d."
                              " It will be replaced by 255", status)
                    status = 255
                log.debug("SSH command '%s' returned status %d%s%s", command, status,
                          (f", stdout: {out[:4096]}" if capture_out else ""),
                          (f", stderr: {err[:4096]}" if capture_err else ""))

            if timed_out:
                raise SSHTimeoutError(self._host, command, out, err, timeout)

            return status, out, err
        except SSHTimeoutError as e:
            log.debug("SSH command timed out: %s", e)
            if not self._raise_exceptions:
                return 255, e.stdout, e.stderr
            raise
        except Exception as e:
            log.debug("Failed to execute SSH command '%s': %s", command, e)
            self._last_error = e
            if not self._raise_exceptions:
                return 255, b"", b""
            raise
        finally:
            if stdin is not None:
                stdin.channel.close()
                stdin.close()
                stdout.close()
                stderr.close()
            if not self._keep_connection:
                self._close()

    def call(self, command, **run_kwargs):
        return self.run(command, **run_kwargs)[0]

    def check_call(self, command, **run_kwargs):
        status, _, _ = self.run(command, **run_kwargs)
        if status != 0:
            raise subprocess.CalledProcessError(status, command)

    def check_output(self, command, **run_kwargs):
        status, stdout, _ = self.run(command, capture_out=True, **run_kwargs)
        if status != 0:
            raise subprocess.CalledProcessError(status, command, output=stdout)
        return stdout

    def scp_to_remote(self, src, dst, preserve_perms=False):
        try:
            self._connect()
            with self._ssh_client.open_sftp() as sftp:
                sftp.put(src, dst)
                if preserve_perms:
                    stat = os.stat(src)
                    sftp.chmod(dst, stat.st_mode)
                    sftp.utime(dst, (stat.st_atime, stat.st_mtime))
            return 0
        except SSHExecutorError as e:
            log.debug("SCP to %s failed: %s", dst, e)
            self._last_error = e
            if not self._raise_exceptions:
                return 255
            raise
        except Exception as e:
            log.debug("SCP to %s failed: %s", dst, e)
            self._last_error = e
            if not self._raise_exceptions:
                return 1
            raise
        finally:
            if not self._keep_connection:
                self._close()

    def scp_from_remote(self, src, dst):
        try:
            self._connect()
            with self._ssh_client.open_sftp() as sftp:
                sftp.get(src, dst)
            return 0
        except SSHExecutorError as e:
            log.debug("SCP from %s failed: %s", src, e)
            self._last_error = e
            if not self._raise_exceptions:
                return 255
            raise
        except Exception as e:
            log.debug("SCP from %s failed: %s", src, e)
            self._last_error = e
            if not self._raise_exceptions:
                return 1
            raise
        finally:
            if not self._keep_connection:
                self._close()

    def scp_and_call(self, script_path):
        if self.scp_to_remote(script_path, "/tmp/caas-script"):
            log.error("Failed to scp %s to %s." % (script_path, self.host))
            return False

        if self.call("chmod 700 /tmp/caas-script && /tmp/caas-script && rm /tmp/caas-script"):
            log.error("Failed to run %s on %s." % (script_path, self.host))
            return False

        return True

    def scp_and_call_on_chroot(self, script_path, root):
        temp_script = "tmp/caas-script"
        dest_path = os.path.join(root, temp_script)

        if self.scp_to_remote(script_path, dest_path):
            log.error("Failed to scp %s to %s." % (script_path, self.host))
            return False

        cmd = "chroot {root} /bin/bash -c 'chmod 700 {script} && {script} && rm {script}'".format(
            root=root, script=os.path.join("/", temp_script))
        if self.call(cmd):
            log.error("Failed to run %s on %s." % (script_path, self.host))
            return False

        return True
