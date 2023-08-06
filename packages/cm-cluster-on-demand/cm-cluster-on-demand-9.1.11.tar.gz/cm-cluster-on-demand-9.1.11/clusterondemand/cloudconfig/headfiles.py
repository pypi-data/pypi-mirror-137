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

import http.client as httplib
import logging
import os
import re
from urllib.parse import urlparse

import requests

from clusterondemand.clusternameprefix import get_prefix
from clusterondemand.copyfile import copy_file_set_version, fill_env_variables
from clusterondemand.exceptions import CODException
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")

CMD_READY_PROBE_PATH = "/root/cm/cmd_ready"
CMD_READY_PROBE = """\
#!/bin/bash
date
echo "Waiting for CMDaemon on `hostname` to update configuration files and start services..."
if [ "$(curl -m 61 -s -o /dev/null -w %{http_code} http://localhost:8080/ready?wait=60\&name=RamdiskService\&name=SysConfigGenerator\&name=SysConfigWriter\&name=dhcpd\&name=named\&name=nfs\&name=nslcd\&name=shorewall)" == "404" ]; then
    echo "The CMDaemon on `hostname` doesn't support the ready service. Will wait for 30 seconds to allow CMDaemon to set up base services."
    sleep 30
    echo "Done, will assume CMDaemon on `hostname` is ready."
    exit 0
fi
while [ "$(curl -m 61 -s -o /dev/null -w %{http_code} http://localhost:8080/ready?wait=60\&name=RamdiskService\&name=SysConfigGenerator\&name=SysConfigWriter\&name=dhcpd\&name=named\&name=nfs\&name=nslcd\&name=shorewall)" != "200" ]; do
    date
    echo "CMDaemon on `hostname` is not ready yet. Will wait some more..."
    sleep 3
done
date
echo "CMDaemon on `hostname` is ready."
"""  # noqa: E501

REMOTE_NODE_DISK_SETUP_PATH = "/root/cm/node-disk-setup.xml"
URL_REGEX = r"^http\:\/\/.*"


# When nodes are created from an image, the resulting root file-system
# will typically have the size of the image. We inject this script to
# grow the file-system to span the entire disk. This is done by finding
# any disk that has a single partition with an XFS file-system, because
# our images are created with XFS. When cluster-extension is done from
# the cod cluster, this script may end up on cloud nodes. We therefore
# skip any node-installer disks.
CATEGORY_INITIALIZE_SCRIPT_PATH = "/root/cm/category-initialize-script"
CATEGORY_INITIALIZE_SCRIPT = """\
#!/bin/bash

# This script is setup by the cluster-on-demand client. It finds disks with a
# single XFS partition (that's not the node-installer) and grows the file-
# system to span the entire disk.
disks=$(lsblk -lno name,type | grep 'disk$' | awk '{print $1}')
for disk in ${disks}; do
  echo -n "Detected disk /dev/${disk}"
  nr_of_partitions=$(lsblk -lno name,type /dev/${disk} | grep -c 'part$')
  if [ "${nr_of_partitions}" -eq "1" ]; then
    partition=$(lsblk -lno name,type /dev/${disk} | grep 'part$' | awk '{print $1}')
    if file --special-files --dereference /dev/$partition | grep --quiet --ignore-case "xfs"; then
      if [ "$(lsblk -lno label /dev/${partition})" != "BCMINSTALLER" ]; then
        echo ", resizing partition /dev/${partition}."
        echo "resizepart 1 -1" | parted /dev/${disk}

        echo -e "\nMounting /dev/${partition}."
        tries=5
        while [[ "${tries}" -gt "0" ]]; do
          if ! mount /dev/${partition} /mnt; then
            ((tries--))
            echo "Mounting /dev/${partition} failed, ${tries} attempts left."
            sleep 1
          else
            echo "Mounted /dev/${partition}."
            break
          fi
        done
        if [[ "${tries}" -eq "0" ]]; then
          echo "Failed to mount /dev/${partition}, aborting."
          exit 1
        fi

        echo "Resizing XFS file-system on /dev/${partition}."
        xfs_growfs /mnt

        echo "Unmounting /dev/${partition}."
        umount /mnt
      else
        echo ", partition /dev/${partition} has node-installer label, skipping resize."
      fi
    else
      echo ", partition /dev/${partition} is not XFS, skipping resize."
    fi
  else
    echo ", contains ${nr_of_partitions} partitions, skipping resize."
  fi
done
"""


def _get_node_disk_setup():
    if config["node_disk_setup_path"]:
        with open(config["node_disk_setup_path"]) as file_handle:
            log.info("Using disk setup from %s" % config["node_disk_setup_path"])
            node_disk_setup = file_handle.read()
    elif config["node_disk_setup"]:
        log.debug("Using disk setup from --node-disk-setup")
        node_disk_setup = config["node_disk_setup"]
    else:
        raise CODException("Please specify a valid node disk setup using --node-disk-setup or "
                           "--node-disk-setup-path.")
    # FIXME: need to remove newlines as somehow the file ends up
    # with '\n' characters if there is newline anywhere, which breaks the setup
    return str(node_disk_setup.replace("\n", ""))


def _get_cm_setup_conf_content():
    temp = {}

    def _ensure_structure(dictionary, module_name):
        if "modules" not in dictionary:
            dictionary["modules"] = {}
        if module_name not in dictionary["modules"]:
            dictionary["modules"][module_name] = {}

    if config["inject_cod_prefix_as_aws_provider_tag"]:
        cod_prefix = get_prefix()
        if not cod_prefix:
            raise CODException("'inject_cod_prefix_as_aws_provider_tag' is set, but the COD_PREFIX is not set")
        _ensure_structure(temp, "clusterextension")
        cluster_extension = temp["modules"]["clusterextension"]
        if "provider_tags" not in cluster_extension:
            cluster_extension["provider_tags"] = []

        cluster_extension["provider_tags"] += ["COD_PREFIX=%s" % cod_prefix]

    return temp


def validate_copy_file_parameters(bright_version, raise_on_missing=True):
    if config["copy_file_with_env"]:
        file_pairs = copy_file_set_version(config["copy_file_with_env"], bright_version)
    elif config["copy_file"]:
        file_pairs = config["copy_file"]
    else:
        return

    if config["copy_file"] or config["copy_file_with_env"]:
        compiled_url_regex = re.compile(URL_REGEX)
        for source, destination in file_pairs:
            if compiled_url_regex.match(source):
                parsed_uri = urlparse(source)
                c = httplib.HTTPConnection(parsed_uri.netloc)
                c.request("HEAD", parsed_uri.path)
                if c.getresponse().status != 200:
                    if raise_on_missing:
                        raise CODException("URL '%s' is unreachable, please make sure "
                                           "the provided URL is valid." % source)
                    else:
                        log.warn("URL '%s' is unreachable, the file will not be copied to the cluster." % source)
                else:
                    log.debug("Copying file '%s' to '%s' on the head node.", source, destination)
            else:
                if not os.path.isfile(source):
                    if raise_on_missing:
                        raise CODException(
                            "The file '%s' does not exist, please make sure the specified path is valid." % source)
                    else:
                        log.warn("The file '%s' does not exist, it will not be copied to the cluster." % source)
                elif destination.startswith("/home"):
                    log.warning("Copying file '%s' to '%s' on the head node.", source, destination)
                    log.warning("Destination file '%s' is in a home directory. Did you mean '/root'?", destination)
                else:
                    log.debug("Copying file '%s' to '%s' on the head node.", source, destination)


def _append_to_write_files(cloud_config, file_pairs, cluster_version=None, get_env=False, preserve_permissions=False):
    """Append files to the write_files in the heat stack in order to write them on the headnode.

    :param cloud_config: CloudConfig object to add the files to
    :param file_pairs: A series of either colon separated src:dst paths
    :param cluster_version: Cluster version
    :param get_env: Specify whether or not to we want to import environment variables
    :param preserve_permissions: Specify whether or not to preserve source file permissions
    """
    file_pairs = copy_file_set_version(file_pairs, cluster_version)
    compiled_url_regex = re.compile(URL_REGEX)
    for file_pair in file_pairs:
        source_file, destination_file = file_pair
        source_permissions = None

        if compiled_url_regex.match(source_file):
            r = requests.get(source_file)
            if r.status_code != 200:
                raise CODException("URL '%s' is unreachable, please make sure "
                                   "the provided URL is valid." % source_file)
            raw_content = r.text.encode()
        else:
            if not os.path.isfile(source_file):
                continue
            if preserve_permissions:
                source_permissions = "{:04o}".format(os.stat(source_file).st_mode)[-4:]
            with open(source_file, "rb") as fdata:
                raw_content = fdata.read()

        if get_env:
            raw_content = fill_env_variables(destination_file, raw_content.decode()).encode()
        cloud_config.add_file(
            destination_file,
            raw_content,
            base64=True,
            permissions=source_permissions
        )


def add_common_head_files(cloud_config, bright_version):
    cloud_config.add_file(CMD_READY_PROBE_PATH, str(CMD_READY_PROBE))
    cloud_config.add_file(REMOTE_NODE_DISK_SETUP_PATH, _get_node_disk_setup())
    cloud_config.add_file(CATEGORY_INITIALIZE_SCRIPT_PATH, CATEGORY_INITIALIZE_SCRIPT)

    cm_setup_conf = _get_cm_setup_conf_content()
    if cm_setup_conf:
        # no yaml.dump for content, as it's not clear how to force proper encoding
        # of newlines for unknown reason it works differently than e.g. for cluster_info
        cloud_config.add_file("/root/cm-setup.conf", cm_setup_conf, permissions="0600")

    if config["copy_file"]:
        _append_to_write_files(
            cloud_config,
            config["copy_file"],
            cluster_version=bright_version,
            preserve_permissions=True,
        )
        # no yaml.dump for content, as it's not clear how to force proper encoding
        # of newlines for unknown reason it works differently than e.g. for cluster_info

    if config["copy_file_with_env"]:
        _append_to_write_files(
            cloud_config,
            config["copy_file_with_env"],
            get_env=True,
            cluster_version=bright_version,
            preserve_permissions=True,
        )

    if config["license_activation_password"]:
        cloud_config.add_file(
            "/var/spool/cmd/license-activation-server.pass",
            config["license_activation_password"],
            permissions="0600", base64=True)
