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

from __future__ import absolute_import, division

import getpass
import itertools
import logging
import os
import re
import signal
import socket
import string
import sys
import time
import traceback
import yaml
from datetime import datetime, timedelta
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
from subprocess import CalledProcessError, check_call
from typing import Dict, List

import netaddr
from dateutil.parser import parse
from dateutil.tz import tzlocal, tzutc
from six.moves import input

from clusterondemand.exceptions import CODException
from clusterondemandconfig import ConfigNamespace, config

from .decorators import retry, static_vars

log = logging.getLogger("cluster-on-demand")

DATE_TIME_FORMAT = "%m-%d %H:%M"
MAX_CLUSTER_NAME_LENGTH = 64

# reserved for SIGINT signal handler
MAX_DELAY_SECS = 2
_interrupts = 0
_last_seen = 0

UUID_RE = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", re.IGNORECASE)

UBUNTU_DEV_REPO = """
deb http://dev.brightcomputing.com/bright/apt/${repo_type}/$$(ARCH)/${bcm_version}/ubuntu/${ubuntu_version}/base/ ./
""".strip()

confirm_ns = ConfigNamespace("confirm", "Confirm operations")
confirm_ns.add_switch_parameter(
    "yes",
    flags=["-y"],
    help="Do not ask for confirmation when executing operations"
)


def is_uuid(string):
    return UUID_RE.match(string) is not None


def valid_cluster_name_regex():
    # Following RFC952 and RFC1123, a cluster name may only consist of alphabetic characters, digits
    # and dashes. It may not start or end with a dash. Additionally, we also don't allow cluster
    # names that consist of only digits.
    # (Note that all these restrictions are also enforced by cmdaemon.)
    only_digits_name = r"^[0-9]+$"
    single_char_name = r"[a-zA-Z]"
    multi_char_name = r"[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]"

    return r"(?!%s)^(%s|%s)$" % (only_digits_name, single_char_name, multi_char_name)


def is_valid_cluster_name(cluster_name):
    return (
        cluster_name and
        len(cluster_name) <= MAX_CLUSTER_NAME_LENGTH and
        bool(re.match(valid_cluster_name_regex(), cluster_name))
    )


def is_valid_ip_address(ip):
    try:
        netaddr.IPAddress(ip)
        return True
    except (netaddr.core.AddrFormatError, ValueError):
        return False


def is_valid_positive_integer(num):
    try:
        if int(num) <= 0:
            return False
        return True
    except ValueError:
        return False


def is_writable_directory(fullpath):
    return os.path.exists(fullpath) and os.path.isdir(fullpath) and os.access(fullpath, os.W_OK)


def format_timestamp(timestamp, format=DATE_TIME_FORMAT):
    """
    Format timestamp.

    :param date:   UNIX timestamp
    :param format:
    :return:       formatted local date/time
    """
    return datetime.fromtimestamp(timestamp).strftime(format)


def format_to_local_date_time(date, tz=None, format=DATE_TIME_FORMAT):
    """
    Format data to local date/time.

    :param date:   ISO 8601 date  (with or without timezone; no timezone means local time)
    :param tz: tzinfo (default: tzlocal())
    :param format:
    :return:       formatted local date/time
    """
    d = parse(date)
    tz = tz or tzlocal()
    if d.tzinfo is not None:
        d = d.astimezone(tz)
    return d.strftime(format)


def get_time_ago_from_iso(date):
    """
    Return human readable version of how long 'date' was ago.

    :param date: ISO 8601 date  (with or without timezone; no timezone means local time)
    :return:  "1d 12h"    (human string time from now
    """
    d1 = parse(date)
    d2 = datetime.now(d1.tzinfo)

    return get_time_ago(d1, d2)


def get_time_ago(past, now=None):
    """Return human readable version of how long 'past' was ago."""
    N_SEC_PER_DAY = 60 * 60 * 24
    N_SEC_PER_HOUR = 60 * 60
    N_SEC_PER_MINUTE = 60

    now = now or datetime.now(past.tzinfo)
    delta = now - past

    seconds = delta.days * N_SEC_PER_DAY + delta.seconds
    days, seconds = divmod(seconds, N_SEC_PER_DAY)
    hours, seconds = divmod(seconds, N_SEC_PER_HOUR)
    minutes, seconds = divmod(seconds, N_SEC_PER_MINUTE)

    if hours == 23 and 30 < minutes:
        return "%dd 0h" % (days + 1)
    elif days:
        return "%dd %dh" % (days, hours)
    elif 30 < seconds:
        return "%dh %dm" % (hours, minutes + 1)
    else:
        return "%dh %dm" % (hours, minutes)


def setup_signal_handlers():
    def sigint_signal_handler(*args):
        global _interrupts
        global _last_seen

        log.debug("Caught SIGINT!")

        now = time.time()
        if now > _last_seen + MAX_DELAY_SECS:
            _interrupts = 0

        _last_seen = now
        _interrupts += 1
        if _interrupts == 1:
            log.info("\n\n\033[91mPress ctrl+c again, quickly, to abort\033[0m\n")

        elif _interrupts > 1:
            log.info("Aborted by user (ctrl+c).")
            raise KeyboardInterrupt

    signal.signal(signal.SIGINT, sigint_signal_handler)


def confirm(message=""):
    if message:
        log.info(message)

    if config["yes"]:
        log.debug("The option --yes is set. Skipping confirmation...")
        return True

    while True:
        log.info("Proceed? [yes/no]")

        reply = input().lower()
        if reply == "no" or reply == "n":
            log.info("Aborted.")
            return False
        elif reply == "yes" or reply == "y":
            return True
        else:
            log.info("Please type 'yes' or 'no'.")


def confirm_with_enter(message=""):
    if message:
        log.info(message)

    if config["yes"]:
        log.debug("The option --yes is set. Skipping confirmation...")
        return

    while True:
        try:
            log.info("Press ENTER to continue, ctrl+c to abort.")

            reply = input().lower()
            if reply != "" and reply != "q":
                log.info("ENTER to continue, ctrl+c (or type 'q') to abort.")
                continue
            elif reply == "q":
                log.info("Aborted.")
                exit(1)
            else:
                return
        except KeyboardInterrupt:
            log.info("Aborted.")
            exit(1)


def confirm_cluster_creation(num_clusters=1):
    if config["yes"]:
        log.debug("The option --yes is set. Skipping confirmation...")
        return

    while True:
        try:

            if num_clusters == 1:
                log.info("Press ENTER to continue and create the cluster.")
            else:
                log.info("Press ENTER to continue and create %s clusters." % num_clusters)

            log.info("Press ctrl+c (or type 'a') to abort. Type 'i' for more info.")

            reply = input().lower()
            if reply != "" and reply != "a" and reply != "i":
                continue
            elif reply == "a":
                log.info("Aborted.")
                exit(1)
            elif reply == "i":
                log.info("")
                log.info('You can set "ask_to_confirm_cluster_creation: false" in the config file'
                         " to permanently disable this question.")
                log.info("Add '-y' to the command line to skip this question in the future.")
                log.info("")

            else:
                return
        except KeyboardInterrupt:
            log.info("Aborted.")
            exit(1)


def confirm_edge_creation():
    if config["yes"]:
        log.debug("The option --yes is set. Skipping confirmation...")
        return

    while True:
        try:
            log.info("Press ENTER to continue and create the edges.")
            log.info("Press ctrl+c (or type 'a') to abort. Type 'i' for more info.")

            reply = input().lower()
            if reply != "" and reply != "a" and reply != "i":
                continue

            elif reply == "a":
                log.info("Aborted.")
                exit(1)

            elif reply == "i":
                log.info("")
                log.info('You can set "ask_to_confirm_edge_creation: false" in the config file'
                         " to permanently disable this question.")
                log.info("Add '-y' to the command line to skip this question in the future.")
                log.info("")

            else:
                return
        except KeyboardInterrupt:
            log.info("Aborted.")
            exit(1)


def wait_for_socket(ip, port, timeout, throw=False):
    @retry(timeout=timeout, only_retry_on_exception=socket.error, wait_between_retries=1.0)
    def try_to_connect(attempts, time_left):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((ip, port))
            log.debug("Connection to %s:%s open. Finished waiting." % (ip, port))
        except socket.timeout as e:
            if 0 == attempts % 10:
                log.debug("Connection to %s:%s is not yet open, waiting for %d seconds" % (ip, port, time_left))
            raise type(e)("Timed out while waiting for %s:%s." % (ip, port))
        except socket.error:
            if 0 == attempts % 10:
                log.debug("Connection to %s:%s is not yet open, waiting for %d seconds" % (ip, port, time_left))
            raise

    try:
        try_to_connect()
        return True
    except socket.timeout as e:
        if throw:
            raise
        log.warning(str(e))
        return False


def to_yaml(value):
    """
    Convert given value (usually a dict) to YAML, correctly handling multi-line strings.

    :param val:   Object to dump as YAML
    :return:      YAML string
    """
    # for some reason the yaml.dump() below doesn't play well
    # with dict's descendant classes
    if isinstance(value, dict) and type(value) is not dict:
        value = dict(value)

    class MultiLineStringDumper(yaml.Dumper):
        def __init__(self, stream, **kwargs):
            super(self.__class__, self).__init__(stream, **kwargs)
            self.__class__.add_representer(str, self._str_presenter)

        def ignore_aliases(self, data):
            # We don't want yaml aliases, they could be confusing to some people. (CM-12080)
            return True

        @staticmethod
        def _str_presenter(dumper, data):
            if len(data.splitlines()) > 1:  # check for multiline string
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    return yaml.dump(value, default_flow_style=False, Dumper=MultiLineStringDumper)


def cod_log(logger, action, percentage):
    logger.info("## Progress: %s", percentage)
    logger.info("#### stage: %s""", action)


def get_package_type(bcm_distro):
    if bcm_distro.upper().startswith("CENTOS"):
        return "yum"
    if bcm_distro.upper().startswith("ROCKY"):
        return "yum"
    elif bcm_distro.upper().startswith("SLES"):
        return "zypper"
    elif bcm_distro.upper().startswith("SL"):  # This has to come after SLES
        return "yum"
    elif bcm_distro.upper().startswith("RHEL"):
        return "yum"
    elif bcm_distro.upper().startswith("UBUNTU"):
        return "apt"
    else:
        raise KeyError("Unknown distro %s" % bcm_distro)


def enumerate_repo_config_files(bcm_distro, root_dir="/", suffix="", sles_suffix="", prefix_root_dir=True):
    if not sles_suffix:
        sles_suffix = suffix
    os_repo_config_mapping = {
        "yum": [
            "etc/yum.repos.d/cm{}.repo".format(suffix)
        ],
        "zypper": [
            "etc/zypp/repos.d/Cluster_Manager{}_Updates.repo".format(sles_suffix)
        ],
        "apt": [
            "etc/apt/sources.list.d/cm{}.list".format(suffix)
        ]
    }

    if prefix_root_dir:
        prefix_dir = root_dir
    else:
        prefix_dir = "/"

    software_images = [
        os.path.join(prefix_dir, "cm/images", elem) for elem in
        os.listdir(os.path.join(root_dir, "cm/images"))
    ]
    node_installer = [os.path.join(prefix_dir, "cm/node-installer")]
    root_paths = [prefix_dir] + software_images + node_installer

    package_type = get_package_type(bcm_distro)
    repo_files = os_repo_config_mapping[package_type]

    for root_path in root_paths:
        for repo_file in repo_files:
            config_file = os.path.join(root_path, repo_file)
            yield config_file


@static_vars(escape_slash_re=re.compile(r"([^\\])\/"))
def sed_file_inplace(path, old, new, plain_text=False):
    def escape_all_slashes(s):
        while True:
            s, count = sed_file_inplace.escape_slash_re.subn(r"\1\/", s)
            if count == 0:
                return s

    if plain_text:
        old = re.escape(old)
        new = re.escape(new)

    try:
        old = escape_all_slashes(old)
        new = escape_all_slashes(new)
        expression = "s/%s/%s/g" % (old, new)
        check_call(["sed", "-i", "-E", expression, path])
    except CalledProcessError as e:
        log.warning(str(e))
        raise


def _define_dev_repository(repo, repo_type, bcm_distro, bcm_version):

    major_version, _ = _extract_bcm_version(bcm_version)

    if bcm_distro.lower().startswith("ubuntu"):

        # The regex below is expecting it in lowercase
        bcm_distro = bcm_distro.lower()
        # The regex below is expecting ubuntu1604 instead of ubuntu16.04
        bcm_distro = bcm_distro.replace(".", "")
        # Retrieve distro/version path from distro string (e.g., ubuntu1604 -> ubuntu/1604)
        ubuntu_version = re.match(r"([a-z]+)([0-9]+)", bcm_distro, re.I).groups()[1]

        # Comment out all updates-*.brightcomputing.com repo lines
        sed_file_inplace(
            repo,
            "^(deb http://([^@]+@)?updates[^.]*.brightcomputing.com)",
            "# \\1"
        )
        dev_repo_line = string.Template(UBUNTU_DEV_REPO).substitute(
            repo_type=repo_type,
            bcm_version=major_version,
            ubuntu_version=ubuntu_version,
        )
        with open(repo, "r+") as repo_file:
            if not any([line.strip() == dev_repo_line for line in repo_file.readlines()]):
                repo_file.write("\n" + dev_repo_line)
    else:
        sed_file_inplace(repo, major_version, bcm_version, plain_text=True)


def _extract_bcm_version(bcm_version):
    pattern = r"(.*(?=\-))(.*)"

    try:
        return re.match(pattern, bcm_version).groups()
    except AttributeError:
        log.error(
            "Failed to extract version from BCM version '%s'" % bcm_version
        )
        raise


def define_dev_repositories(bcm_distro, bcm_version, root_dir):
    try:
        cm_repos = enumerate_repo_config_files(bcm_distro, root_dir)
        ml_repos = enumerate_repo_config_files(bcm_distro, root_dir, suffix="-ml", sles_suffix="_ML")
    except KeyError:
        log.warning(
            "Not changing repository configuration files for unknown distro '%s'" % (bcm_distro, )
        )

    for repo, repo_type in itertools.chain(
        zip(cm_repos, itertools.repeat("cm")),
        zip(ml_repos, itertools.repeat("ml"))
    ):
        if not os.path.isfile(repo):
            log.debug("Skipping '%s', does not exist" % (repo, ))
            continue
        log.debug("Enabling %s repository in '%s'" % (bcm_version, repo))
        _define_dev_repository(repo, repo_type, bcm_distro, bcm_version)


def get_user_at_fqdn_hostname():
    return "{user}@{host}".format(
        user=getpass.getuser(),
        host=socket.getfqdn()
    )


class MultithreadRunError():
    """Used by multithread_run to indicate error."""
    def __init__(self, traceback, exception):
        self.traceback = traceback
        self.exception = exception


def multithread_run(function, args_list, max_threads):
    """Runs a function multiple times in different threads and waits for them.

    For each tuple in 'args_list', a new thread will be created to run function(*args_list[i]) with a maximum
    of 'max_threads' in parallel.

    The most common use case is to run the same function with different arguments. But It's possible to run
    different functions by passing them in the 'args_list' and setting a dummy function in 'function':
    multithread_run(lambda f: f(), [func1, func2])
    """

    pool = ThreadPool(max_threads)

    def wrapped(args):
        try:
            if not isinstance(args, tuple):
                args = (args,)
            return function(*args)
        except Exception as e:
            return MultithreadRunError(traceback.format_exc(), e)

    result = pool.map_async(wrapped, args_list)

    # We run result.get with a timeout, otherwise Python ignores signals (meaning that CTRL+C is ignored)
    # Just adding a timeout is enough, so even result.get(9999999) would work, but I prefered to do the loop
    # just in case.
    # https://stackoverflow.com/questions/14421133/catch-keyboard-interrupt-in-program-that-is-waiting-on-an-event
    ret = None
    while ret is None:
        try:
            ret = result.get(600)
        except TimeoutError:
            log.debug("Timed out waiting for asynchronous result. Waiting again...")
            continue

    return ret


def running_in_virtual_env():
    if "VIRTUAL_ENV" in os.environ:
        return True
    return False


def partition(func, iterable):
    true_items = []
    false_items = []
    for item in iterable:
        if func(item):
            true_items.append(item)
        else:
            false_items.append(item)
    return true_items, false_items


def resolve_hostname(hostname: str, retries=4, retry_delay_sec=0.2) -> str:
    ip = None
    while True:
        try:
            ip = socket.gethostbyname(hostname)
            log.debug(f"Successfully resolved '{hostname}' to '{ip}'.")
            break
        except socket.error as e:
            log.debug(f"Failed to resolve hostname '{hostname}' to an IP. Reason: {e}")
            if retries > 0:
                log.debug(f"... Retry in {retry_delay_sec} seconds.")
                retries -= 1
                time.sleep(retry_delay_sec)
            else:
                raise CODException(f"Failed to resolve hostname '{hostname}' to an IP address.")
    return ip


def resolve_hostnames(hostnames: List[str]) -> Dict[str, str]:
    return {name: resolve_hostname(name) for name in hostnames}


def get_commands_to_inject_resolved_hostnames(roots: List[str], resolved_hostname_ips: Dict[str, str]) -> List[str]:
    commands = []

    for root in roots:
        if root == "/":
            root = ""
        commands += [f"echo '# This section was added by cod-os' >> {root}/etc/hosts"]
        for hostname, ip in resolved_hostname_ips.items():
            commands += [f"echo '{ip}                     {hostname}' >> {root}/etc/hosts"]
        commands += [f"echo '# The end of entries added by cod-os' >> {root}/etc/hosts"]
    return commands


def log_no_clusters_found(command_name):
    log.info(f"There were no eligible clusters to perform the '{command_name}' operation" +
             (f" with the arguments: {', '.join(config['filters'])}"
              if config.is_item_set_explicitly("filters") else ""))


def generate_timedelta(string):
    regex = re.compile(r"((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?")
    match = regex.match(string.replace(" ", "")).groupdict()

    days = int(match.get("days") or 0)
    hours = int(match.get("hours") or 0)
    minutes = int(match.get("minutes") or 0)
    delta = timedelta(days=days, hours=hours, minutes=minutes)

    return delta


def generate_older_than_date(delta):
    if not delta:
        return None

    return (datetime.utcnow() - delta).replace(tzinfo=tzutc())


def report_progress(status, previous_status=""):
    """
    Report progress only if the progress is printed to a terminal.
    """
    if not sys.stderr.isatty:
        return ""

    if status != previous_status:
        sys.stderr.write("\r" + status)

    return status
