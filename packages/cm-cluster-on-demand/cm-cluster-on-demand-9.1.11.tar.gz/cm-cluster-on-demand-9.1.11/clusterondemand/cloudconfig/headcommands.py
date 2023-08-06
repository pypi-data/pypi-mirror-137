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

import netaddr

from clusterondemand.cloudconfig import CMD_READY_PROBE_PATH
from clusterondemand.clustercreate import enable_cmd_debug_commands, set_cmd_advanced_config_commands
from clusterondemand.utils import get_commands_to_inject_resolved_hostnames, resolve_hostnames
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


def add_head_node_commands(cloud_config, internal_ip):
    """ Let's first signal the status wait condition that cloud init started """
    cloud_config.add_status_commands("cloud-init: Started.")

    cloud_config.add_status_commands("cloud-init: Setting up eth0.")
    ip_net = netaddr.IPNetwork(str(config["internal_cidr"]))
    assert internal_ip in ip_net, "%s is not in subnet %s" % (internal_ip, ip_net)

    cloud_config.add_commands([
        "echo Set head node IP",
        "ip link set up dev eth0",
        "ip address flush dev eth0",
        "ip addr add %s/%s dev eth0" % (internal_ip, ip_net.netmask),
    ])

    mtu = config["internal_mtu"]
    if mtu is not None:
        cloud_config.add_status_commands("cloud-init: Setting eth0 custom mtu.")
        cloud_config.add_command("ip link set mtu %d dev eth0" % mtu)

    if config["ssh_password_authentication"]:
        cloud_config.add_status_commands("cloud-init: Enabling password authentication.")
        cloud_config.add_commands([
            "echo 'COD-OS: SSH password authentication requested, editing sshd config file'",
            "sed -i 's/^PasswordAuthentication no/# Bright Cluster on Demand: enabling due to "
            "ssh-password-authentication\\nPasswordAuthentication yes/g' /etc/ssh/sshd_config",
            "echo 'Reloading the sshd service'",
            "if ! systemctl try-reload-or-restart sshd; then",
            "  echo 'Old systemd, using different reload command.'",
            "  systemctl reload-or-try-restart sshd",
            "fi",
        ])

    if config["ssh_pub_key_path"]:
        with open(config["ssh_pub_key_path"]) as pub_key:
            cloud_config.add_command("echo '%s' >> /root/.ssh/authorized_keys" % pub_key.read())

    if config["append_to_root_bashrc"]:
        cloud_config.add_command("echo '# START of entries added by append_to_root_bashrc of Cluster on Demand' "
                                 ">> /root/.bashrc")
        for line in config["append_to_root_bashrc"]:
            cloud_config.add_command("echo '%s' >> /root/.bashrc" % line)
        cloud_config.add_command("echo '# END of entries added by append_to_root_bashrc of Cluster on Demand' "
                                 ">> /root/.bashrc")

    if config["cmd_debug"]:
        subsystems = config["cmd_debug_subsystems"]
        log.debug(f"Setting debug mode on CMDaemon for subsystems: '{subsystems}'")
        for command in enable_cmd_debug_commands(subsystems):
            cloud_config.add_command(command)

    # In this mode the CMD monitoring system will sample metric at randomized intervals
    # And it also says to CMD that hanged compute nodes must be reset
    log.debug("Setting VirtualCluster mode on CMDaemon")
    for command in set_cmd_advanced_config_commands(["VirtualCluster=1"]):
        cloud_config.add_command(command)


def add_run_bright_setup_commands(cloud_config):
    # We have to load these modules so the command cm-bright-setup is available
    # Some older versions don't have the module cm-setup (it's all part of cluster-tools)
    # and would fail to load. That's why "|| true"
    cloud_config.add_commands([
        "echo Loading modules",
        "source /etc/profile.d/modules.sh",
        "module load cluster-tools",
        "module load cm-setup || true",
    ])

    if config["resolve_hostnames"]:
        # This can work around DNS issues by resolving hostnames during cluster creation
        commands = get_commands_to_inject_resolved_hostnames(
            ["/", "/cm/images/default-image"],
            resolve_hostnames(config["resolve_hostnames"]))
        for command in commands:
            cloud_config.add_command(command)

    if config["prebs"]:
        cloud_config.add_status_commands("cloud-init: Running prebs commands.")
        cloud_config.add_command("echo 'Starting custom prebs commands'")
        cloud_config.add_commands(config["prebs"])

    cloud_config.add_status_commands("cloud-init: Running cm-bright-setup.")
    cloud_config.add_command("cm-bright-setup -c /root/cm/cm-bright-setup.conf --on-error-action abort")
    cloud_config.add_status_commands("cloud-init: cm-bright-setup complete.")

    if config["postbs"]:
        cloud_config.add_status_commands("cloud-init: Running postbs commands.")
        cloud_config.add_command("echo 'Starting custom postbs commands'")
        cloud_config.add_commands(config["postbs"])


def add_wait_for_cmd_ready_commands(cloud_config):
    cloud_config.add_status_commands("cloud-init: Waiting for CMDaemon to be ready.")
    cloud_config.add_command("chmod +x " + CMD_READY_PROBE_PATH)
    cloud_config.add_command(CMD_READY_PROBE_PATH)
    cloud_config.add_status_commands("cloud-init: CMDaemon is ready.")
