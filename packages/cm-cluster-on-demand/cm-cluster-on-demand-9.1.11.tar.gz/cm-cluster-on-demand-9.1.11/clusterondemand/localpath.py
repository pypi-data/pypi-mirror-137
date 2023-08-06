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

from .exceptions import UserReportableException


def localpath(string):
    """A parser for paths that exist on the local machine."""
    return os.path.expanduser(string)


def must_exist(parameter, configuration):
    if configuration[parameter.key] and not os.path.isfile(configuration[parameter.key]):
        raise UserReportableException(
            "{name}={value} does not exist".format(name=parameter.key, value=configuration[parameter.key])
        )


def must_be_readable(parameter, configuration):
    if configuration[parameter.key] and not os.access(configuration[parameter.key], os.R_OK):
        raise UserReportableException(
            "{name}={value} is not readable".format(name=parameter.key, value=configuration[parameter.key])
        )
