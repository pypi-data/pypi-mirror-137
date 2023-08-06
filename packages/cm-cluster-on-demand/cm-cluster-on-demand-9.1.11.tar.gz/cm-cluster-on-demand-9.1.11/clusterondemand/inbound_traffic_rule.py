#!/usr/bin/env python
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

import logging
import re
from copy import deepcopy

from clusterondemand.exceptions import CODException

# Regular expression matching the following format:
#   [SRC_CIDR[:SRC_PORT_OR_PORT_RANGE],]DST_PORT_OR_PORT_RANGE[:PROTOCOL]
IPV4_CIDR = r"(\d{1,3}(\.\d{1,3}){3}(?:/\d{1,2})"
PORT_OR_PORT_RANGE = r"\d{1,5}(-\d{1,5})?)?"
PORT = r"\d{1,5}"
PROTOCOL = "(tcp|udp)"

SOURCE_REGEX = "^(" + IPV4_CIDR + "(:" + PORT_OR_PORT_RANGE + ",)?"
DESTINATION_REGEX = "(" + PORT_OR_PORT_RANGE + "(:" + PROTOCOL + ")?)$"

INBOUND_RULE_REGEX = SOURCE_REGEX + DESTINATION_REGEX

ANY = "*"

log = logging.getLogger("cluster-on-demand")


class InboundTrafficRule(object):

    def __init__(self, inbound_rule):

        if not self.validate_inbound_rule(inbound_rule):
            raise CODException("Inbound rule '{inbound_rule}' does not match the expected format.\n"
                               "The expected format is: [src_cidr[:src_port],]dst_port[:protocol]\n"
                               "Examples: '80' '21:udp' '11.0.0.0/24,20-23:TCP' "
                               "'12.0.0.0/32:6000-6500,443'".format(inbound_rule=inbound_rule))
        self.inbound_rule = inbound_rule
        self._parse_rule()

    def _parse_rule(self):
        if "," in self.inbound_rule:
            source_rule, destination_rule = self.inbound_rule.split(",")
        else:
            source_rule = "{src_cidr}:{src_port}".format(src_cidr="0.0.0.0/0", src_port=ANY)
            destination_rule = self.inbound_rule
        self.src_cidr, self.src_first_port, self.src_last_port = self.parse_source(source_rule)
        self.dst_first_port, self.dst_last_port, self.protocol = self.parse_destination(destination_rule)
        if not self.dst_first_port <= self.dst_last_port and self.src_first_port <= self.src_last_port:
            raise CODException("Invalid inbound traffic rule: port_range_min must be <= port_range_max")

    @staticmethod
    def parse_port(port):
        if "-" in port:
            first_port, last_port = port.split("-")
        else:
            first_port = last_port = port
        return first_port, last_port

    def parse_source(self, source_rule):
        if ":" in source_rule:
            cidr, port = source_rule.split(":")
        else:
            cidr, port = source_rule, ANY
        self.src_port = port
        first_port, last_port = self.parse_port(port)
        return cidr, first_port, last_port

    def parse_destination(self, destination_rule):
        if ":" in destination_rule:
            port, protocol = destination_rule.split(":")
        else:
            port, protocol = destination_rule, ANY
        self.dst_port = port
        first_port, last_port = self.parse_port(port)
        return first_port, last_port, protocol

    @staticmethod
    def validate_inbound_rule(inbound_rule):
        return re.match(INBOUND_RULE_REGEX, inbound_rule, re.IGNORECASE)

    def __str__(self):
        return self.inbound_rule

    @staticmethod
    def process_inbound_rules(inbound_rules):
        if not inbound_rules:
            return []
        processed_inbound_rules = deepcopy(inbound_rules)
        for inbound_rule in processed_inbound_rules:
            if any(port != "*" for port in [inbound_rule.src_first_port, inbound_rule.src_last_port]):
                log.warning("Source port was specified in rule {traffic_rule} but is only supported by Azure "
                            "so will be ignored.".format(traffic_rule=inbound_rule))

            # if the protocol is not specified in the rule, it has to be split into two separate rules (tcp/udp)
            if inbound_rule.protocol == "*":
                inbound_rule.protocol = "tcp"
                inbound_rule_copy = deepcopy(inbound_rule)
                inbound_rule_copy.protocol = "udp"
                processed_inbound_rules.append(inbound_rule_copy)

        return processed_inbound_rules
