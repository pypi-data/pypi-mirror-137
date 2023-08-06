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

import re
from functools import total_ordering
from logging import getLogger

from clusterondemand.exceptions import CODException

log = getLogger("cluster-on-demand")


@total_ordering
class ImageDistroSpec:
    """Utility class for parsing and comparing image distro specifications."""

    _DISTRO_REGEX = [
        re.compile(r"^(?P<family>(?:rocky|alma)?centos)(?:(?P<major>\d+)(?:u(?P<minor>\d+))?)?$"),
        re.compile(r"^(?P<family>rhel)(?:(?P<major>\d+)(?:u(?P<minor>\d+))?)?$"),
        re.compile(r"^(?P<family>sles)(?:(?P<major>\d+)(?:sp(?P<minor>\d+))?)?$"),
        re.compile(r"^(?P<family>ubuntu)(?:(?P<major>\d\d)(?P<minor>\d\d)?)?$"),
        re.compile(r"^(?P<family>sl)(?:(?P<major>\d+)(?:u(?P<minor>\d+))?)?$"),
        re.compile(r"^(?P<family>rocky|alma)(?:(?P<major>\d+)(?:u(?P<minor>\d+))?)?$"),
    ]

    _DISTRO_FORMAT = {
        "centos": "{}u{}",
        "rhel": "{}u{}",
        "sles": "{}sp{}",
        "ubuntu": "{}{:02d}",
        "sl": "{}u{}",
        "rocky": "{}u{}",
        "rockycentos": "{}u{}",
        "alma": "{}u{}",
        "almacentos": "{}u{}",
    }

    def __init__(self, distro):
        if distro is None:
            self._family = None
            self._major = None
            self._minor = None
            return
        for regex in self._DISTRO_REGEX:
            match = regex.match(distro)
            if match:
                self._family = match["family"]
                self._major = int(match["major"]) if match["major"] else None
                self._minor = int(match["minor"]) if match["minor"] else None
                assert self._family and (not self._minor or self._minor and self._major), (
                    f"Invalid distro regex: {regex}")
                break
        else:
            raise CODException(f"Unable to determine base distribution from '{distro}'")

    def __eq__(self, value):
        if isinstance(value, str):
            value = ImageDistroSpec(value)
        return (self.family == value.family and
                self.major == value.major and
                self.minor == value.minor)

    def __gt__(self, value):
        if isinstance(value, str):
            value = ImageDistroSpec(value)
        if self.family != value.family:
            raise Exception(f"Cannot compare distros '{self}' and '{value}'")
        major1 = self.major or 0
        minor1 = self.minor or 0
        major2 = value.major or 0
        minor2 = value.minor or 0
        return major1 > major2 or (major1 == major2 and minor1 > minor2)

    def __contains__(self, value):
        if isinstance(value, str):
            value = ImageDistroSpec(value)
        return ((self.family is None or self.family == value.family) and
                (self.major is None or self.major == value.major) and
                (self.minor is None or self.minor == value.minor))

    def __str__(self):
        result = self.family
        if self.major is not None:
            result += str(self.major)
            if self.minor is not None:
                result = self._DISTRO_FORMAT[self.family].format(result, self.minor)
        return result

    @property
    def family(self):
        return self._family

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def family_and_major(self):
        if self.family and self.major:
            return self.family + str(self.major)
        return None

    @property
    def full(self):
        return str(self) if self.is_full else None

    @property
    def is_full(self):
        return self.major is not None and self.minor is not None


def latest_distro(list_of_distros, distro):
    """
    Given a list of distros, we return the latest for a given distro specification
    `distro` can be:
    - Distro family: "centos"
    - Distro family and major: "centos7"
    - Full distro name: "centos7u7"
    - None: In this case we return the latest from the list

    list_of_distros has to be all in the full name format and all the same distro family
    """
    if not list_of_distros:
        return None

    list_of_distros = [ImageDistroSpec(d) for d in list_of_distros]
    if distro:
        distro_spec = ImageDistroSpec(distro)
    else:
        distro_spec = ImageDistroSpec(list_of_distros[0].family)

    list_of_distros = [d for d in list_of_distros if d in distro_spec]
    return max(list_of_distros) if list_of_distros else None
