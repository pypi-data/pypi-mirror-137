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
import re

from clusterondemand import const
from clusterondemand.utils import partition

log = logging.getLogger("cluster-on-demand")


def format_cluster_tags(dict_tags, unparsed_tags=None):
    if unparsed_tags is None:
        unparsed_tags = []

    list_tags, single_tags = partition(lambda x: isinstance(dict_tags[x], list), dict_tags)

    collapsed_dict_tags = ["%s=%s" % (tag, dict_tags[tag]) for tag in single_tags]
    for tag in list_tags:
        collapsed_dict_tags += ["%s#%s" % (tag, value) for value in dict_tags[tag]]

    tags = collapsed_dict_tags + unparsed_tags
    return tags


def format_packagegroups_tags(package_groups):
    return [f"{const.COD_PACKAGE_GROUP}={group}" for group in package_groups]


def parse_cluster_tags(tags):
    """Parse the cluster tags to a shape easier to handle.

    Clusters will have tags like 'COD::XX=YY', this returns a dict where dict['COD::XX'] = YY
    Tags that don't follow this key=value form, are returned in a list

    Since the package group tag can appear more than once, it's not included.
    Use get_packagegroups_from_tags(tags) to get that data.

    Tags are allowed to be repeated using the format ['COD::XX#YY', 'COD::XX#ZZ']. In that
    case it will be returned as dict['COD::XX'] = ['YY', 'ZZ']

    :param tags: list of cluster tags
    :return: Tuple (dict_tags, unparsed_tags)
    """
    if not tags:
        return ({}, [])

    single_tags_regex = re.compile("(?!" + const.COD_PACKAGE_GROUP + ")(COD::.+)=(.+)")
    list_tags_regex = re.compile("(COD::.+)#(.+)")

    single_tags = [tag for tag in tags if single_tags_regex.match(tag)]
    list_tags = [tag for tag in tags if list_tags_regex.match(tag)]

    # Add single tags
    dict_tags = {k: v for (k, v) in [single_tags_regex.match(tag).groups() for tag in single_tags]}

    # Add list tags
    for tag in list_tags:
        k, v = list_tags_regex.match(tag).groups()
        if k not in dict_tags:
            dict_tags[k] = []
        dict_tags[k].append(v)

    # Check for unparsed tags
    unparsed_tags = [tag for tag in tags if tag not in single_tags and tag not in list_tags]

    return dict_tags, unparsed_tags


def get_packagegroups_from_tags(tags):
    """Return the list of package groups from the cluster tags."""
    if not tags:
        return []
    regex = re.compile(const.COD_PACKAGE_GROUP + "=(.+)")
    return [m.group(1) for m in [regex.match(tag) for tag in tags] if m]
