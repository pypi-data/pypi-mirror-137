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

import netaddr

from .exceptions import UserReportableException


def nullable_cidr(string):
    """A parser for cidr strings which allows None values as well."""
    if string.lower() == "none":
        return None
    return cidr(string)


def cidr(string):
    """A parser for cidr strings."""
    try:
        network = netaddr.IPNetwork(string)
        if str(network.cidr) != str(network):
            raise UserReportableException("'%s' is not a valid CIDR: the host section is not empty" % (string))
        return network
    except netaddr.core.AddrFormatError:
        raise UserReportableException("'%s' is not a valid CIDR" % (string))


def must_be_within_cidr(parent_cidr_name):
    """Validation that raises an error when the CIDR value of the parameter is not contained within the parent CIDR"""
    def wrapper(parameter, configuration):
        parent = configuration.get_item_for_key(parent_cidr_name).parameter
        subnet_cidr = configuration[parameter.key]
        parent_cidr = configuration[parent.key]

        if subnet_cidr is None:
            raise UserReportableException("%s is not set" % (parameter.key))
        if parent_cidr is None:
            raise UserReportableException("%s is not set" % (parent.key))

        if subnet_cidr.network < parent_cidr.network or subnet_cidr.broadcast > parent_cidr.broadcast:
            raise UserReportableException(
                "%s=%s not within %s=%s. Use %s and/or %s to change that." % (
                    parameter.key, subnet_cidr,
                    parent.key, parent_cidr,
                    parent.default_flag, parameter.default_flag
                )
            )

    return wrapper
