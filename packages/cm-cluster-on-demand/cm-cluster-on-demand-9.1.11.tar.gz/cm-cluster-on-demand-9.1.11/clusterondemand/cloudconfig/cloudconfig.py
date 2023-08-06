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

import copy
from abc import ABC, abstractmethod
from base64 import b64encode


class SignalHandler(ABC):
    def __init__(self, status_log_prefix: str):
        self.log_prefix = status_log_prefix
        super().__init__()

    @abstractmethod
    def get_init_commands(self):
        pass

    @abstractmethod
    def get_files(self):
        pass

    @abstractmethod
    def get_status_log_commands(self, status: str):
        pass

    @abstractmethod
    def get_config_complete_commands(self):
        pass


class CloudConfig(dict):
    def __init__(self, signal_handler: SignalHandler):
        self.signal_handler = signal_handler
        self["write_files"] = []
        self["bootcmd"] = []
        self["runcmd"] = signal_handler.get_init_commands()
        self["disable_ec2_metadata"] = False
        for file in signal_handler.get_files():
            self.add_file(file["path"], file["content"])

    def add_status_commands(self, status: str):
        self.add_commands(self.signal_handler.get_status_log_commands(status))

    def add_config_complete_commands(self):
        self.add_commands(self.signal_handler.get_config_complete_commands())

    def enable_metadata(self, enable_metadata):
        self["disable_ec2_metadata"] = not enable_metadata

    def add_file(self, path, content, base64=False, permissions=None):
        write_file = {
            "path": path
        }

        if base64:
            write_file["encoding"] = "base64"
            write_file["content"] = b64encode(content)
        else:
            write_file["content"] = content

        if permissions is not None:
            write_file["permissions"] = permissions

        self["write_files"].append(write_file)

    def add_boot_command(self, command):
        self["bootcmd"].append(command)

    def add_boot_commands(self, commands):
        self["bootcmd"] += commands

    def add_command(self, command):
        self["runcmd"].append(command)

    def add_commands(self, commands):
        self["runcmd"] += commands

    def to_dict(self):
        result = copy.deepcopy(self)
        return dict(result)
