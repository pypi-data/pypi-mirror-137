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

from clusterondemand.bcm_version import BcmVersion
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


def get_license_dict(name=None):
    license_dict = {
        "cluster_name": str(name if name else config["name"]),
        "unit": str(config["license_unit"]),
        "locality": str(config["license_locality"]),
        "country": str(config["license_country"]),
        "product_key": str(config["license_product_key"]),
        "state": str(config["license_state"]),
        "organization": str(config["license_organization"])
    }
    # COD images older than 8.1-11 will break because of unrecognized "license_activation_token"
    # configuration key. To prevent it, don't pass it unless it was specified.
    if config["license_activation_token"]:
        license_dict["activation_token"] = str(config["license_activation_token"])
        if config["license_activation_url"]:
            license_dict["activation_url"] = str(config["license_activation_url"])
    return license_dict


def generate_bright_setup(cloud_type,
                          wlm,
                          license_dict,
                          hostname,
                          password,
                          node_count,
                          timezone,
                          admin_email=None,
                          node_disk_setup_path=None,
                          node_kernel_modules=None):
    brightsetup = {
        "cloud_type": cloud_type,
        "bright": {
            "wlm": wlm,
            "wlm_slot_count": 1,
            # None   type gets translated to 'None' string somewhere,
            # that's why need need empty string here for pbsproc_lic_server
            "pbspro_lic_server": "",
            "license": license_dict,
            "hostname": str(hostname),  # otherwise it will end up as unicode:  u"xxxx"
            "master_compute_node": False,
            "password": password,
            "node_count": node_count
        },
    }

    if node_kernel_modules:
        brightsetup["bright"]["node_kernel_modules"] = node_kernel_modules
    else:
        # TODO:fixme: CM-9026 otherwise somehow the default config value does not kick in
        # (we get key error)
        brightsetup["bright"]["node_kernel_modules"] = []
    if node_disk_setup_path:
        brightsetup["bright"]["node_disk_setup_path"] = node_disk_setup_path
    else:
        # TODO:fixme: CM-9026 otherwise somehow the default config value does not kick in
        # (we get key error)
        brightsetup["bright"]["node_disk_setup_path"] = ""
    if timezone:
        brightsetup["bright"]["timezone"] = timezone
    if admin_email:
        brightsetup["bright"]["admin_email"] = admin_email

    if BcmVersion(config["version"]) > "8.1" and config["http_proxy"] is not None:
        brightsetup["bright"]["http_proxy"] = config["http_proxy"]
    elif config["http_proxy"] is not None:
        log.warning("http_proxy is not supported for versions prior to 8.2.")

    return {
        "modules": {
            "brightsetup": brightsetup
        }
    }
