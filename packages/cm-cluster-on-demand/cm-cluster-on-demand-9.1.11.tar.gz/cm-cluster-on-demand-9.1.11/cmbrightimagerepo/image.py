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

from copy import deepcopy
from logging import getLogger

from six.moves.urllib.parse import urljoin

log = getLogger("cluster-on-demand")


class ImageDescriptionVersionMismatchError(Exception):
    """Version of the description object is not supported."""

    def __init__(self, version):
        super(ImageDescriptionVersionMismatchError, self).__init__(
            "Version %s of image description is not supported", version
        )


class Image(object):
    """Image description object.

    It can be constructed from the description returned from Repository.
    """

    @classmethod
    def make_from_descripton(cls, descr, baseurl):
        """Create image object from descr object."""
        if descr["version"] != 1:
            raise ImageDescriptionVersionMismatchError(descr["version"])

        if baseurl is not None:
            descr = deepcopy(descr)
            descr["url"] = urljoin(baseurl, descr["url"])
        return cls(descr)

    @classmethod
    def make_from_descripton_noraise(cls, descr, baseurl):
        """Create image object from descr object."""
        try:
            return cls.make_from_descripton(descr, baseurl)
        except Exception as e:
            log.warning("Could not parse image description %s: %s", descr, e)

    @classmethod
    def bootstrap_image(cls,
                        id,
                        url,
                        tags,
                        package_groups,
                        bcm_version,
                        bcm_release,
                        image_type,
                        os,
                        revision,
                        cmd_revision,
                        created_at,
                        cloud_type):
        return cls.make_from_descripton({
            "version": 1,
            "id": id,
            "url": url,
            "tags": tags,
            "package_groups": package_groups,
            "bcm_version": bcm_version,
            "bcm_release": bcm_release,
            "image_type": image_type,
            "os": os,
            "revision": revision,
            "cmd_revision": cmd_revision,
            "created_at": created_at,
            "cloud_type": cloud_type,
        }, baseurl=None)

    def uncompressed_image_info_missing(self):
        return self._description.get("uncompressed_size") is None

    def image_info_missing(self):
        return self._description.get("size") is None or \
            self._description.get("md5sum") is None

    def set_uncompressed_image_info(self, uncompressed_size):
        self._description["uncompressed_size"] = uncompressed_size

    def set_image_info(self, size, md5sum):
        self._description["size"] = size
        self._description["md5sum"] = md5sum

    def __init__(self, description):
        self._description = description

    def raw_description(self):
        return self._description

    def id(self):
        """Return unique string across the repo."""
        return self._description["id"]

    def url(self):
        """Return URL of the image file."""
        return self._description["url"]

    def tags(self):
        """Return tags of the image."""
        return self._description["tags"]

    def md5sum(self):
        """Return MD5 checksum of the image file."""
        return self._description["md5sum"]

    def size(self):
        """Size of the image file in bytes."""
        return self._description["size"]

    def uncompressed_size(self):
        return self._description["uncompressed_size"]

    def package_groups(self):
        """Return package groups preinstalled to the image."""
        return self._description["package_groups"]

    def bcm_version(self):
        """Bright version installed to the image."""
        return self._description["bcm_version"]

    def bcm_release(self):
        """Bright release installed to the image."""
        return self._description.get("bcm_release", 0)

    def image_type(self):
        """Type of bcm image."""
        return self._description["image_type"]

    def os(self):
        """Operating system of the image."""
        return self._description["os"]

    def revision(self):
        """Image revision."""
        return self._description["revision"]

    def created_at(self):
        """Image creation timestamp."""
        return self._description["created_at"]

    def cmd_revision(self):
        """Return CMDaemon revision installed in the image."""
        return self._description["cmd_revision"]

    def cloud_type(self):
        """Cloud type this image was created for."""
        return self._description["cloud_type"]

    def completed(self):
        """Object is consistent and contains all necessary information."""
        def _check_key(key):
            return self._description.get(key) is not None

        keys = [
            "id",
            "url",
            "tags",
            "md5sum",
            "size",
            "uncompressed_size",
            "package_groups",
            "bcm_version",
            "image_type",
            "os",
            "revision",
            "created_at",
            "cmd_revision",
            "version",
            "cloud_type",
        ]
        for key in keys:
            if not _check_key(key):
                return False

        return True
