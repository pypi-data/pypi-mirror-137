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

from __future__ import absolute_import

import os
import re
import subprocess

from .exceptions import UserReportableException

SSH_KEYGEN_REGEX = r"(?P<length>[0-9]+) [^:]+:(?P<fingerprint>\S+) .* \((?P<type>[^\)]+)\)$"


class CODSSHPrivateKeys(object):

    def __init__(self):

        self.keys = {}

        default_keyfiles = [
            "id_dsa",
            "id_ecdsa",
            "id_ed25519",
            "id_rsa"
        ]

        fingerprint_hash = "md5"

        for keyfile_basename in default_keyfiles:
            keyfile = os.path.expanduser("~/.ssh/{}".format(keyfile_basename))
            self._add_key_to_dict(keyfile, fingerprint_hash)

        agent_keys = self._get_ssh_agent_keys(fingerprint_hash)
        if agent_keys:
            self.keys.update(agent_keys)

    def fingerprint_exists(self, check_fingerprint):
        return check_fingerprint in self.keys

    def _add_key_to_dict(self, keyfile, fingerprint_hash):
        if os.path.exists(keyfile):
            ssh_keygen_output = _run_ssh_keygen(keyfile, fingerprint_hash)

            if ssh_keygen_output:
                key_length, key_fingerprint, key_type = ssh_keygen_output
                self.keys[key_fingerprint] = {
                    "type": key_type,
                    "length": int(key_length)
                }

    @staticmethod
    def _get_ssh_agent_keys(fingerprint_hash):
        if "SSH_AUTH_SOCK" not in os.environ:
            return None

        ssh_agent_keys = {}

        ssh_add_proc = subprocess.Popen(["ssh-add", "-E", fingerprint_hash, "-l"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ssh_add_proc.communicate()
        if stdout:
            lines = stdout.decode("utf-8").split("\n")
            for line in lines:
                ssh_add_match = re.match(SSH_KEYGEN_REGEX, line)
                if ssh_add_match:
                    key_length = ssh_add_match.group("length")
                    key_fingerprint = ssh_add_match.group("fingerprint")
                    key_type = ssh_add_match.group("type")
                    ssh_agent_keys[key_fingerprint] = {
                        "type": key_type,
                        "length": int(key_length)
                    }

        return ssh_agent_keys


class CODSSHPubKey(object):

    def __init__(self, keyfile, fingerprint="sha256"):

        self.ssh_keygen_success = False
        self.key_length = None
        self.key_fingerprint = None
        self.key_type = None

        ssh_keygen_output = _run_ssh_keygen(keyfile, fingerprint)

        if ssh_keygen_output:
            self.ssh_keygen_success = True
            self.key_length, self.key_fingerprint, self.key_type = ssh_keygen_output

    def is_valid(self):
        return self.ssh_keygen_success


def _run_ssh_keygen(keyfile, fingerprint):
    ssh_keygen_proc = subprocess.Popen(["ssh-keygen", "-E", fingerprint, "-l", "-f", keyfile],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = ssh_keygen_proc.communicate()
    if stdout:
        ssh_keygen_match = re.match(SSH_KEYGEN_REGEX, stdout.decode("utf-8"))
        if ssh_keygen_match:
            key_length = ssh_keygen_match.group("length")
            key_fingerprint = ssh_keygen_match.group("fingerprint")
            key_type = ssh_keygen_match.group("type")
            return int(key_length), key_fingerprint, key_type

    return None


def validate_ssh_pub_key(parameter, configuration, allowed_types=None):
    keyfile = configuration[parameter.key]

    if keyfile:

        if not os.path.exists(keyfile):
            raise UserReportableException("SSH key file {} does not exist".format(keyfile))

        pubkey = CODSSHPubKey(keyfile)

        if not pubkey.is_valid():
            raise UserReportableException("SSH key file {} is not a valid key file".format(keyfile))

        if allowed_types and (pubkey.key_type not in allowed_types
                              or pubkey.key_length < allowed_types[pubkey.key_type]):
            allowed_types_list = list(map(lambda key: "{}:{}".format(key, allowed_types[key] or "any"), allowed_types))
            raise UserReportableException("SSH key file {} is of type {} and bitsize {}, "
                                          "permitted types and minimum bitsize are {}".format(
                                              keyfile,
                                              pubkey.key_type,
                                              pubkey.key_length,
                                              ", ".join(allowed_types_list)
                                          ))
