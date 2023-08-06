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

from __future__ import absolute_import, division

from functools import reduce

import six

from clusterondemand.codoutput.sortingutils import SortableData
from clusterondemand.utils import get_time_ago

ALL_COLUMNS = [
    ("id_revision", "ImageID:Revision"),
    ("name", "Image name"),
    ("type", "Image type"),
    ("head_size", "Head(GB)"),
    ("node_size", "Node(GB)"),
    ("size", "Size(GB)"),
    ("distro", "Distro"),
    ("cmd_revision", "CMD Rev."),
    ("bcm_version", "BCM Version"),
    ("created_at", "Created"),
    ("uploaded_at", "Uploaded"),
    ("package_groups", "Packages"),
    ("is_public", "Public"),
    ("uuid", "UUID"),
    ("cloud_type", "Cloud Type"),
]

ADVANCED_COLUMNS = [
    "name", "type", "size", "distro", "cmd_revision", "bcm_version", "created_at", "uploaded_at",
    "package_groups", "is_public", "uuid", "cloud_type",
]

BASIC_COLUMNS = [
    "id_revision", "head_size", "node_size", "distro", "cmd_revision", "bcm_version", "created_at",
    "package_groups", "is_public"
]

USER_READABLE_IMAGE_TYPES = {
    "node": "Compute node",
    "headnode": "Head node",
    "node-installer": "Node installer",
    "edge-iso": "Edge ISO",
}


def user_readable_image_type(image_type):
    return USER_READABLE_IMAGE_TYPES.get(image_type) or ""


def make_images_table(images, sortby=None, columns=None, output_format=None):
    sortby = sortby or []
    columns = columns or [column[0] for column in ALL_COLUMNS]
    rows = [
        [getattr(image, column[0], "N/A") for column in ALL_COLUMNS]
        for image in images
    ]

    table = SortableData(all_headers=ALL_COLUMNS, requested_headers=columns, rows=rows)
    table.sort(*sortby)
    return table.output(output_format=output_format)


def make_cod_images_table(cod_images, sortby=None, columns=None, advanced=False, output_format="table"):
    if not columns:
        columns = ADVANCED_COLUMNS if advanced else BASIC_COLUMNS

    return make_images_table(
        [CODImageAdapter(image, advanced) for image in cod_images],
        sortby=sortby,
        columns=columns,
        output_format=output_format
    )


class CODImageAdapter(object):
    """Adapter that maps every key in ALL_COLUMNS to a value of a COD Image."""

    def __init__(self, image, advanced=False):
        self.name = image.name
        if image.bcm_optional_info:
            self.id_revision = "{0.id}:{0.revision} ({0.bcm_optional_info})".format(image)
        else:
            self.id_revision = "{0.id}:{0.revision}".format(image)
        self.revision = image.revision

        if 0 == len(image.node_images):
            node_images_size = None
        else:
            node_images_size = reduce(lambda acc, cur: acc + cur, [i.size for i in image.node_images], 0)
        self.size = GigabyteSize(image.size + (node_images_size or 0))
        self.head_size = GigabyteSize(image.size)
        self.node_size = GigabyteSize(node_images_size)

        self.distro = image.distro
        self.cmd_revision = image.cmd_revision
        self.bcm_version = image.version
        self.created_at = RelativeDateTime(image.created_at)
        self.uploaded_at = RelativeDateTime(image.uploaded_at)
        self.package_groups = ",".join(image.package_groups)
        self.is_public = image.image_visibility == "public"
        self.uuid = image.uuid
        self.cloud_type = image.cloud_type

        image_types = [image.type]
        if not advanced:
            # In the non-advanced we show the image sets, so we put all the types here
            image_types += [node_image.type for node_image in image.node_images]
        self.type = ", ".join(user_readable_image_type(t) for t in image_types)


class GigabyteSize(object):
    """Utility class that allows both sorting by value while still giving the value a custom string representation."""

    N_BYTES_PER_GB = 1024 ** 3

    def __init__(self, bytes):
        self.bytes = bytes

    if six.PY2:
        def __cmp__(self, other):
            return cmp(self.bytes, other.bytes)  # noqa: F821
    elif six.PY3:
        def __lt__(self, other):
            return self.bytes < other.bytes

    def __str__(self):
        if self.bytes is None:
            return "N/A"
        else:
            return str(round(self.bytes / GigabyteSize.N_BYTES_PER_GB, 2))


class RelativeDateTime(object):
    """Utility class that allows both sorting by value while still giving the value a custom string representation."""

    def __init__(self, time):
        self.time = time

    if six.PY2:
        def __cmp__(self, other):
            return cmp(self.time, other.time)  # noqa: F821
    elif six.PY3:
        def __lt__(self, other):
            return self.time < other.time

    def __str__(self):
        return get_time_ago(self.time) + " ago" if self.time else "N/A"
