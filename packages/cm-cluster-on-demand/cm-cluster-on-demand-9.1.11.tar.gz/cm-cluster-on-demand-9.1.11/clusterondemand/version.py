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

import os
import yaml
from collections import OrderedDict

import six

PATH_TO_VERSION_INFO = os.path.join(os.path.dirname(os.path.realpath(__file__)), "version-info.yaml")

HUMAN_READABLE_INFO = OrderedDict([
    ("version", "Version"),
    ("branch", "Branch"),
    ("git_hash", "Git Hash"),
    ("git_date", "Git Date"),
    ("build_date", "Build Date"),
])


def get_version_info():
    """Returns dictionary containing the version information."""
    try:
        return yaml.safe_load(open(PATH_TO_VERSION_INFO).read())
    except FileNotFoundError:
        return {
            "version": "9.1",
            "branch": "",
            "git_hash": "",
            "git_date": "",
            "build_date": ""
        }


def print_version_info():
    version_info = get_version_info()
    for key, human_text in six.iteritems(HUMAN_READABLE_INFO):
        value = version_info.get(key)
        if value:
            print("{}: {}".format(human_text, value))
