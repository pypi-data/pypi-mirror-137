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

from __future__ import absolute_import, print_function

from enum import Enum, auto

from dateutil.tz import tzlocal
from prettytable import PrettyTable

from clusterondemand.utils import get_time_ago

SEPARATOR = "##SEP##"


class SummaryType(Enum):
    Proposal = auto()
    Overview = auto()


class SummaryGenerator(object):
    """Generate the summary for creation of clusters and nodes."""

    def __init__(self,
                 head_name,
                 config=None,
                 head_image=None,
                 ip=None,
                 nas_node_definition=None,
                 node_definitions=None,
                 node_image=None,
                 primary_head_node_definition=None,
                 secondary_head_node_definition=None,
                 region=None,
                 summary_type=None,
                 ssh_string=None,
                 trace_id=None):
        self._config = config
        self._head_name = head_name
        self._head_image = head_image
        self._ip = ip
        self._nas_node_definition = nas_node_definition
        self._node_definitions = node_definitions if node_definitions else []
        self._node_image = node_image
        self._primary_head_node_definition = primary_head_node_definition
        self._secondary_head_node_defintion = secondary_head_node_definition
        self._region = region
        self._type = summary_type
        self._ssh_string = ssh_string
        self._trace_id = trace_id

    def generate_table(self):
        """Generate a list of lines containing the cluster overview."""
        table = PrettyTable(header=False, border=False)
        table.field_names = ["Property", "Value"]
        table.align["Property"] = "r"
        table.align["Value"] = "l"

        self._add_header(table)
        if self._type == SummaryType.Proposal:
            self._add_image_rows(table)
            self._add_head_node_info(table)
            self._add_compute_node_info(table)
            self._add_nas_node_info_row(table)
        self._add_rows(table)
        if self._type == SummaryType.Overview:
            self._add_access_info(table)
        self._add_separator(table)
        table_lines = str(table).split("\n")

        # Replace each separator line with a row of dashes.
        separator_line = "-" * len(table_lines[0])
        lines = [separator_line if SEPARATOR in line else line for line in table_lines]

        return lines

    def print_summary(self, println=print):
        """
        Print the summary.

        :param println: Function to be used to print each line
        """
        for line in self.generate_table():
            println(line)

    def _add_compute_node_info(self, table):
        for definition in self._node_definitions:
            self._add_node_summary(table, "Nodes:", definition)

    def _add_cluster_name(self, table):
        table.add_row(["Cluster:", self._head_name])

    def _add_access_info(self, table):
        if self._ssh_string:
            table.add_row(["SSH string:", self._ssh_string])
        if self._ip:
            table.add_row(["IP:", self._ip])
        if self._config["ssh_pub_key_path"]:
            table.add_row(["Key path:", self._config["ssh_pub_key_path"]])
        if self._config["ssh_password_authentication"]:
            table.add_row(["Warning:", "SSH password authentication enabled"])
        if self._config["log_cluster_password"]:
            table.add_row(["Password:", self._config["cluster_password"]])

    def _add_rows(self, table):
        """
        Add COD specific infomation to the summary table.
        """
        pass

    def _add_header(self, table):
        self._add_separator(table)
        self._add_cluster_name(table)
        self._add_separator(table)

    def _add_head_node_info(self, table):
        if self._primary_head_node_definition and self._secondary_head_node_defintion:
            self._add_node_summary(table, "Primary head node:", self._primary_head_node_definition)
            self._add_node_summary(table, "Secondary head node:", self._secondary_head_node_defintion)
        elif self._primary_head_node_definition:
            self._add_node_summary(table, "Head node:", self._primary_head_node_definition)

    def _add_image_rows(self, table):
        if self._head_image and self._head_image.name:
            revision = f":{self._head_image.revision}" if self._head_image.revision else ""
            image_details = f"({self._head_image.id}{revision})" if self._head_image.id else ""
            table.add_row(["Image name:", f"{self._head_image.name}{image_details}"])

        if self._node_image and self._node_image.name:
            table.add_row(["Node image:", "%s(%s:%s)" % (
                self._node_image.name,
                self._node_image.id,
                self._node_image.revision,
            )])

        if self._head_image and self._head_image.name:
            img_created = self._head_image.created_at.astimezone(tzlocal()).strftime(format="%Y-%m-%d %H:%M")
            img_age = get_time_ago(self._head_image.created_at)
            pkg_groups = self._head_image.package_groups or "none"

            table.add_row(["Image date:", "%s (%s ago)" % (img_created, img_age)])
            table.add_row(["Package groups:", pkg_groups])

            if self._config and "show_git_hashes" in self._config and self._config["show_git_hashes"]:
                git_hashes = ""
                git_hashes += "cmdaemon: {0}\n".format(self._head_image.cmd_hash or "n/a")
                git_hashes += "cm-setup: {0}\n".format(self._head_image.cm_setup_hash or "n/a")
                git_hashes += "cluster-tools: {0}".format(self._head_image.cluster_tools_hash or "n/a")
                table.add_row(["Git hashes:", git_hashes])

        if self._head_image and self._head_image.version:
            table.add_row(["Version:", self._head_image.version])

        if self._head_image and self._head_image.distro:
            table.add_row(["Distro:", self._head_image.distro])

    def _add_nas_node_info_row(self, table):
        if self._nas_node_definition:
            self._add_node_summary(table, "NAS node:", self._nas_node_definition)

    def _add_node_summary(self, table, field_name, node_definition):
        flavor_string = self._get_flavor_string(node_definition.flavor)
        summary = f"{node_definition.count} ({flavor_string})"

        # If the node count is set to 0 we don't want to add unnecessary information and can exit early.
        if node_definition.count == 0:
            table.add_row([field_name, summary])
            return

        if node_definition.availability_zone:
            summary += f"\nAvailability zone: {node_definition.availability_zone}"

        # The first disk is the root disk, all other disks are extra.
        root_disk = node_definition.disks[0] if node_definition.disks else None
        extra_disks = node_definition.disks[1:]

        if root_disk:
            root_disk_type = f""" (type: {root_disk.get("type")}) """ if root_disk.get("type") else ""
            summary += f"""\nRoot disk: {root_disk.get("size")} GiB{root_disk_type}"""

        for disk in extra_disks:
            if not disk.get("size"):
                continue
            extra_disk_type = f""" (type: {disk.get("type")}) """ if disk.get("type") else ""
            summary += f"""\nExtra disk: {disk.get("size")} GiB{extra_disk_type}"""

        table.add_row([field_name, summary])

    def _add_region(self, table):
        table.add_row(["Region:", self._region])

    def _add_separator(self, table):
        table.add_row([SEPARATOR, ""])

    def _add_trace_id(self, table):
        if self._trace_id:
            table.add_row(["Trace ID:", self._trace_id])

    def _get_flavor_string(self, flavor):
        return str(flavor)
