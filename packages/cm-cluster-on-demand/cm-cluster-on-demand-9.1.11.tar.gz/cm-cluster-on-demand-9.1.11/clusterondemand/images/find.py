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

import re
import yaml
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from itertools import filterfalse
from logging import getLogger

import pytz

from clusterondemand.exceptions import CODException
from clusterondemand.imagetable import CODImageAdapter, make_images_table
from clusterondemand.paramvalidation import (
    validate_headnode_image_value,
    validate_image_value,
    validate_node_image_value
)
from clusterondemandconfig import BCM_VERSION, ConfigNamespace
from cmbrightimagerepo.image import Image

from .distro_family import ImageDistroSpec, latest_distro
from .filters.byid import make_id_query, match_by_id_query
from .filters.packagegroups import match_by_package_groups
from .filters.tags import match_by_tags
from .queryparser import classify_ids, only_explicit_ids

log = getLogger("cluster-on-demand")

HEAD_NODE_IMAGE, COMPUTE_NODE_IMAGE = "head node", "node"


@dataclass
class CODImage:
    bcm_optional_info: str = ""
    cloud_type: str = ""
    cmd_revision: int = -1
    created_at: datetime = None
    distro: str = ""
    distro_family: str = ""
    id: str = ""
    name: str = ""
    image_visibility: str = ""
    revision: int = -1
    size: int = 0
    tags: list = ""
    type: str = ""
    uploaded_at: datetime = None
    uuid: str = ""
    version: str = ""
    package_groups: list = field(default_factory=list)
    cmd_hash: str = ""
    cm_setup_hash: str = ""
    cluster_tools_hash: str = ""
    node_images: list = field(default_factory=list)

    @staticmethod
    def image_name(image_type, image_id, image_revision):
        if image_type == "headnode":
            prefix = "bcmh"
        elif image_type == "node":
            prefix = "bcmn"
        elif image_type == "node-installer":
            prefix = "bcni"
        elif image_type == "edge-iso":
            prefix = "bcm-ni-edge"
        else:
            raise Exception("Unsupported image type %s" % (image_type))
        return f"{prefix}-{image_id}-{image_revision}"

    # TODO Move the code from cmbrightimagerepo.image.Image to here?
    @classmethod
    def from_manifest_data(cls, manifest, baseurl=None):
        image = Image.make_from_descripton(manifest, baseurl)

        # Remove everything after first digit
        # Same logic as in build-cod-image.sh
        distro_family = re.sub(r"\d.*", "", image.os())

        return CODImage(
            bcm_optional_info="",
            cloud_type=image.cloud_type(),
            cmd_revision=image.cmd_revision(),
            created_at=datetime.fromtimestamp(image.created_at(), pytz.utc),
            distro=image.os(),
            distro_family=distro_family,
            id=image.id(),
            name=CODImage.image_name(image.image_type(), image.id(), image.revision()),
            image_visibility="public",
            revision=image.revision(),
            size=image.uncompressed_size(),
            tags=image.tags(),
            type=image.image_type(),
            uploaded_at=datetime.fromtimestamp(image.created_at(), pytz.utc),
            uuid="N/A",
            version=str(image.bcm_version()),
            package_groups=sorted(image.package_groups()),
        )

    @classmethod
    def from_manifest_file(cls, filename, baseurl=None):
        try:
            with open(filename) as manifest_source:
                return cls.from_manifest_data(yaml.safe_load(manifest_source), baseurl)
        except Exception as e:
            raise CODException(
                f"Error loading image description from {filename}: {e}",
                caused_by=e
            )

    def get_properties(self):
        """
        Return dictionary with the image properties. Useful for when creating and tagging an image
        """
        return {
            "bcm_cloud_type": self.cloud_type,
            "bcm_cluster_tools_hash": self.cluster_tools_hash,
            "bcm_cmd_hash": self.cmd_hash,
            "bcm_cmd_revision": str(self.cmd_revision),
            "bcm_cm_setup_hash": self.cm_setup_hash,
            "bcm_created_at": str(self.created_at),
            "bcm_distro": self.distro,
            "bcm_distro_family": self.distro_family,
            "bcm_image_id": self.id,
            "bcm_image_revision": str(self.revision),
            "bcm_image_type": self.type,
            "bcm_optional_info": self.bcm_optional_info,
            "bcm_package_groups": ",".join(self.package_groups),
            "bcm_version": str(self.version),
        }

    def get_tags(self):
        return self.tags


class ImageSource:
    def __init__(self,
                 ids=None,
                 package_groups=None,
                 tags=None,
                 version=None,
                 distro=None,
                 revision=None,
                 status=None,
                 type=None,
                 advanced=False,
                 image_visibility="any",
                 cloud_type="any"):
        assert image_visibility in ["public", "private", "any"]
        # Not sure why this check
        # assert(not type or advanced)

        ids = ["*"] if ids is None else ids

        (self.ids, self.patterns, self.regexes, self.uuids) = classify_ids(ids)
        self.package_groups = package_groups if package_groups is not None else ["any"]
        if self.package_groups == ["none"]:
            self.package_groups = []
        self.tags = tags if tags is not None else []
        self.version = version
        self.distro_spec = ImageDistroSpec(distro)
        self.distro = self.distro_spec.full
        self.distro_family = None if self.distro else self.distro_spec.family
        self.revision = revision
        self.status = status
        self.type = type
        self.advanced = advanced
        self.image_visibility = image_visibility
        self.cloud_type = cloud_type if cloud_type != "any" else None

    @classmethod
    def from_config(cls, config, ids=None):
        """Instantiate a proper ImageSource from a cod config
        Pick images doesn't have config["ids"]. It's passed by parameter
        So the implemenation has to check if the parameter is None.
        Small limitation of this interface
        """
        raise NotImplementedError()

    def _iter_from_source(self):
        """Return generator with the specified images"""
        raise NotImplementedError()

    @classmethod
    def find_images_using_options(cls, config):
        source = cls.from_config(config)
        return source.find_images(config=config)

    def find_images(self, latest=None, latest_invert=False, config=None):
        if config is not None:
            if config["all_revisions"]:
                latest = None
                latest_invert = False
            elif config["except_latest"] is not None:
                latest = config["except_latest"]
                latest_invert = True
            else:
                latest = config["latest"]
                latest_invert = False

        assert self.advanced or not self.uuids

        images = self._iter_from_source()

        def log_skip_image(image, fmt, *args, **kwargs):
            log.debug(("{0.id}:{0.revision} is skipped. Cause: " + fmt)
                      .format(image, *args, **kwargs))
            return False
        image_types = ("headnode", "node", "node-installer", "edge-iso")
        images = (
            image for image in images
            if image.type in image_types or
            log_skip_image(
                image, "image type mismatch: {0.type} is not of the possible image types: '{1}'",
                "', '".join(image_types)
            )
        )

        if not self.advanced:
            def id_key_fun(image):
                return image.id
        else:
            def id_key_fun(image):
                return image.name

        only_by_id = only_explicit_ids(self.ids, self.patterns, self.regexes, self.uuids, self.advanced)

        rev_regexes = make_id_query(self.ids, self.patterns, self.regexes)

        images = (
            image for image in images
            if match_by_id_query(
                rev_regexes,
                id_key_fun(image),
                image.revision
            ) or (self.uuids and image.uuid in self.uuids) or
            log_skip_image(image,
                           "image id mismatch: {0.id} do not match either these regexes: {1}, "
                           "or these uuids: {2}",
                           [(revision, regex.pattern) for revision, regex in rev_regexes],
                           self.uuids)
        )

        def valid_distro(image):
            return (
                self.distro_spec is None or image.distro in self.distro_spec or
                log_skip_image(image, "distro mismatch: {0.distro} not in spec {1}", self.distro_spec)
            )

        if not only_by_id:
            images = (
                image for image in images
                if self.revision is None or image.revision == self.revision or
                log_skip_image(image, "revision mismatch: {0.revision} != {1}", self.revision)
            )
            images = (
                image for image in images
                if self.package_groups is None or match_by_package_groups(self.package_groups, image.package_groups) or
                log_skip_image(image, "package groups mismatch: {0.package_groups} != {1}",
                               self.package_groups)
            )
            images = (
                image for image in images
                if valid_distro(image)
            )
            images = (
                image for image in images
                if match_by_tags(self.tags, image.tags) or
                log_skip_image(image, "tags mismatch: {0.tags} do not match requested: {1}", self.tags)
            )
            images = (
                image for image in images
                if self.version is None or image.version == self.version or
                log_skip_image(image, "version mismatch: {0.version} != {1}", self.version)
            )
            images = (
                image for image in images
                if self.image_visibility == "any" or image.image_visibility == self.image_visibility or
                log_skip_image(image, "public visibility mismatch: {0.image_visibility} != {1}", self.image_visibility)
            )

        # cloud_type filtering is out of the 'if' above because we always to do it, even if the user types a specific id
        images = (
            image for image in images
            if self.cloud_type is None or image.cloud_type == self.cloud_type or
            log_skip_image(image, "cloud type mismatch: {0.cloud_type} != {1}", self.cloud_type)
        )

        if latest is not None:
            images = list(images)
            if self.advanced:
                latest_revisions = get_latest_revisions(latest, latest_invert, images)
            else:
                latest_revisions = get_latest_revisions(latest, latest_invert,
                                                        [i for i in images if i.type == "headnode"])
            images = (
                image for image in images
                if image.revision in latest_revisions.get(image.id, [])
            )

        def create_cod_image(head, nodes):
            head.node_images = nodes
            return head

        if not self.advanced:
            images = (create_cod_image(head, nodes) for head, nodes in group_images(images))
        else:
            images = (create_cod_image(image, []) for image in images)

        return images

    @classmethod
    def pick_head_node_image_using_options(cls, opts):
        head_image_id = opts.get("head_node_image")
        image_id = opts.get("image")

        if head_image_id:
            image_ids = [head_image_id, _image_id_from_image_set_id(head_image_id, HEAD_NODE_IMAGE)]
            return cls._pick_image_by_ids(image_ids, HEAD_NODE_IMAGE, opts["cloud_type"])
        elif image_id:
            image_ids = [_image_id_from_image_set_id(image_id, HEAD_NODE_IMAGE)]
            return cls._pick_image_by_ids(image_ids, HEAD_NODE_IMAGE, opts["cloud_type"])
        else:
            # User did not specify head image explicitly, find one based on version, distro, etc.
            return cls._pick_head_node_image_by_opts(opts)

    @classmethod
    def pick_compute_node_image_using_options(cls, opts):
        node_image_id = opts["node_image"]
        image_id = opts["image"]

        if node_image_id == "none":
            return None
        elif node_image_id:
            image_ids = [node_image_id, _image_id_from_image_set_id(node_image_id, COMPUTE_NODE_IMAGE)]
            return cls._pick_image_by_ids(image_ids, COMPUTE_NODE_IMAGE, opts["cloud_type"])
        elif image_id:
            image_ids = [_image_id_from_image_set_id(image_id, COMPUTE_NODE_IMAGE)]
            return cls._pick_image_by_ids(image_ids, COMPUTE_NODE_IMAGE, opts["cloud_type"])
        else:
            # User did not specify node image explicitly, find one based on version, distro, etc.
            return cls._pick_compute_node_image_by_opts(opts)

    @classmethod
    def _pick_head_node_image_by_opts(cls, opts):
        source = cls.from_config(opts, ids=["*"])
        images = list(source.find_images(latest=True))

        selected_distro = latest_distro([i.distro for i in images], opts["distro"])
        images = [i for i in images if i.distro == selected_distro]

        if 0 == len(images):
            raise NoImagesFoundError.create_for_filter_options(opts, HEAD_NODE_IMAGE)
        elif 1 == len(images):
            return images[0]
        else:
            raise MultipleImagesFoundError.create_for_filter_options(opts, images, HEAD_NODE_IMAGE)

    @classmethod
    def _pick_compute_node_image_by_opts(cls, opts):
        # Select a compute node image based on the --version/--distro/etc
        # This is done by selecting a head node image, and then picking the one was matched to it

        node_head_image = cls._pick_head_node_image_by_opts(opts)

        if not node_head_image or not node_head_image.node_images:
            return None
        else:
            node_images = [img for img in node_head_image.node_images if img.type == "node"]
            assert len(node_images) == 1, "One node image expected, %d found" % len(node_images)
            return node_images[0]

    @classmethod
    def _pick_image_by_ids(cls, image_ids, image_type, cloud_type):
        """Iterate over list of Glance image ids in order. Return the first image found with such an image id.

        When a tried image id maps to multiple images, an error is raised. If multiple image ids in the
        parameter map to an image, the first image is returned. If none of the image ids map to an
        image, an error is raised as well.
        """
        for image_id in image_ids:
            source = cls(ids=[image_id], advanced=True, cloud_type=cloud_type)
            found_images = list(source.find_images())

            if 0 == len(found_images):
                pass
            elif 1 == len(found_images):
                return found_images[0]
            else:
                raise MultipleImagesFoundError.create_for_image_id(image_id, found_images, image_type)
        else:
            raise NoImagesFoundError.create_for_tried_image_ids(image_ids, image_type)


def _image_id_from_image_set_id(image_set_id, image_type):
    """
    Convert an <image set id>:<revision>, into the id of a Glance image

    >>> _image_id_from_image_set_id("centos7u5-trunk:213", HEAD_NODE_IMAGE)
    'bcmh-centos7u5-trunk-213'
    >>> _image_id_from_image_set_id("ubuntu1804-9.0-dev:1", COMPUTE_NODE_IMAGE)
    'bcmn-ubuntu1804-9.0-dev-1'
    """
    prefix = {HEAD_NODE_IMAGE: "bcmh", COMPUTE_NODE_IMAGE: "bcmn"}[image_type]
    return prefix + "-" + re.sub(r":([0-9]+)$", r"-\1", image_set_id)


class NoImagesFoundError(CODException):
    """Raised when no image could be found for either the uuid, image ids or filter."""

    @classmethod
    def create_for_tried_image_ids(cls, tried_ids, image_type):
        tried_ids = list(set(tried_ids))
        if 1 == len(tried_ids):
            return cls("Could not find a %s image for %s" % (image_type, tried_ids[0]))
        else:
            return cls("Could not find a %s image for any of these ids: %s" % (image_type, ", ".join(tried_ids)))

    @classmethod
    def create_for_filter_options(cls, filter_options, image_type):
        return cls("Could not find any %s image matching these criteria:\n%s" %
                   (image_type, _format_filter_string(filter_options)))


class MultipleImagesFoundError(CODException):
    """Raised when the specified image id, or filter options, generated multiple images to chose from."""

    @classmethod
    def create_for_image_id(cls, image_id, images, image_type):
        return cls(
            'More than one %s image matched "%s". Use %s <UUID> to explicitly chose one:\n%s' %
            (image_type, image_id, _flag_for_image_type(image_type), _format_image_list(images))
        )

    @classmethod
    def create_for_filter_options(cls, filter_options, images, image_type):
        return cls(
            "There were several %s images that match these criteria, use %s <UUID> to explicitly chose one:\n%s\n%s\n" %
            (image_type, _flag_for_image_type(image_type), _format_filter_string(filter_options),
             _format_image_list(images))
        )


def _flag_for_image_type(image_type):
    return {HEAD_NODE_IMAGE: "--head-node-image", COMPUTE_NODE_IMAGE: "--node-image"}[image_type]


def _format_filter_string(opts):
    filter_options = ["tags", "version", "distro", "package_groups", "image_visibility"]
    option_and_values = ((opts.get_item_for_key(name).parameter, opts[name]) for name in filter_options)
    filter_string = "\n".join(
        "{namespace}.{config_option}={val}".format(
            namespace=opt.namespaces[-1],
            config_option=opt.key,
            val=val
        )
        for opt, val in option_and_values
    )
    return filter_string


def _format_image_list(images):
    return make_images_table(
        (CODImageAdapter(img) for img in images),
        columns=["id_revision", "name", "uuid"],
        sortby=["id_revision"],
        output_format="table"
    )


def get_latest_revisions(n, invert, images):
    """
    Return a dictonary {<image-id>: [n latest revisions]}

    If `invert`, we return the opposite revisions (all revisions except the last n)
    """
    image_revisions = defaultdict(set)
    for image in images:
        image_revisions[image.id].add(image.revision)

    def last_n(images):
        return sorted(images, reverse=True)[n:] if invert else sorted(images, reverse=True)[:n]

    return {
        image_id: last_n(revisions)
        for image_id, revisions in image_revisions.items()
    }


def group_all_by(source, keyfunc, ismainfunc):
    """Group item list to the [(mainitem, [item,...]), ...] structure, preserving the sort order.

    >>> DATA = [(1, "m", 1), (3, "i", 2), (2, "i", 1), (4, "m", 3)]
    >>> ismainfunc = lambda i: i[1] == "m"
    >>> keyfunc = lambda i: i[2]
    >>> list(group_all_by(DATA, keyfunc, ismainfunc))
    [((1, 'm', 1), [(2, 'i', 1)]), ((4, 'm', 3), [])]

    """
    source = list(source)
    for main_item in filter(ismainfunc, source):
        key = keyfunc(main_item)
        items = filterfalse(ismainfunc, source)
        related_items = filter(
            lambda item: keyfunc(item) == key,
            items
        )
        yield (main_item, list(related_items))


def group_images(images):
    return group_all_by(
        images,
        keyfunc=lambda image: (image.id, int(image.revision)),
        ismainfunc=lambda image: image.type == "headnode"
    )


findimages_ns = ConfigNamespace("common.images.find", help_section="image filter parameters")
findimages_ns.add_parameter(
    "cloud_type",
    help="Filter images by cloud type. Set 'any' for any cloud type. Useful with --advanced"
)
findimages_ns.add_parameter(
    "version",
    help="(default: all versions) show only images from this version"
)
findimages_ns.add_parameter(
    "status",
    default="active",
    help="Status of the image"
)
findimages_ns.add_parameter(
    "distro",
    help=("(default: all distros) show only images from this distro."
          "This is a regex")
)
findimages_ns.add_parameter(
    "revision",
    type=int,
    help="Select images with this revision."
)
findimages_ns.add_enumeration_parameter(
    "package_groups",
    help_varname="PACKAGE_GROUP",
    default=["any"],
    help=("Select images with these package groups installed "
          "(use 'none' to pick an image with no package groups installed, "
          " use 'any' (default) to pick an image with any set of package groups installed.")
)
findimages_ns.add_enumeration_parameter(
    "tags",
    default=[],
    help=("List of tags, the images must have them all. (AND). "
          "--tags any will pick images with any set of tags")
)
findimages_ns.add_repeating_positional_parameter(
    "ids",
    default=["*"],
    help=("List of image specifiers. By default (unless '--advanced' is used) those are "
          "assumed to be in the COD 'ImageID[:revision]' format. Each specifier can be a "
          "plain string (e.g. centos7u5-8.0), a wildcard (e.g. centos*), or a regex (e.g. "
          "centos7u[45]*). It is also possible to explicitly suffix any of the above with "
          "a colon, followed by a number specifying the image revision (e.g. 'centos7u5-8.0:42', "
          "or 'centos*:42', or '*:42'). If the '--advanced' flag is used, the specifiers "
          "will not be treated as COD ImageIDs, but instead they will be treated as "
          "'Name' or 'UUID' strings (or wildcards, or regexes). For example 'bcmh-centos*'.")
)
findimages_ns.add_switch_parameter(
    "all_revisions",
    help="Pick all revisions for each image ID"
)
findimages_ns.add_parameter(
    "latest",
    default=1,
    help="Pick this many latest images for each image ID"
)
findimages_ns.add_switch_parameter(
    "advanced",
    help="Filter image by its name or UUID rather than ImageID. "
    "Will also change listing output."
)
findimages_ns.add_parameter(
    "except_latest",
    type=int,
    help="Pick all images besides this number of the latest images for each image ID"
)
findimages_ns.add_parameter(
    "image_visibility",
    choices=["any", "public", "private"],
    default="any",
    advanced=True,
    help="Whether to show 'any' images (both public and private), "
         "or only 'public' or 'private' images. Defaults to 'any'."
)

pickimages_ns = ConfigNamespace("common.images.pick", help_section="image selection parameters")
pickimages_ns.import_namespace(findimages_ns)
pickimages_ns.remove_imported_parameter("ids")
pickimages_ns.override_imported_parameter("package_groups", default=["none"])
pickimages_ns.override_imported_parameter("version", default=BCM_VERSION)
pickimages_ns.add_parameter(
    "image",
    help_varname="IMAGE_SPEC",
    help=("Single image selector statement. "
          "See cm-cod-os image list --help. "
          "Overrides filter arguments such as --version, --distro, etc."),
    validation=validate_image_value
)
pickimages_ns.add_parameter(
    "head_node_image",
    help_varname="UUID|IMAGE-NAME|IMAGE-SET",
    help=("Single image selector statement for the head node image. Can either be an image "
          "UUID, the name of that image or the name of the image set. Overrides the head node "
          "image selected by --image and all other image filter arguments."),
    validation=validate_headnode_image_value
)
pickimages_ns.add_parameter(
    "node_image",
    help=("Single image selector statement for node image (as in advanced mode) "
          "'--node-image none' will force the cluster to not use a node image at all. "
          "Overrides the head node image selected by --image and all other image "
          "filter arguments."),
    validation=validate_node_image_value
)
