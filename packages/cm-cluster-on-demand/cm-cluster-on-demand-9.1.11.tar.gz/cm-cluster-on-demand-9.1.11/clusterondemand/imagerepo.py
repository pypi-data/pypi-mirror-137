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
from datetime import datetime

import pytz

from clusterondemand.images.find import CODImage, ImageSource
from clusterondemandconfig import ConfigNamespace
from cmbrightimagerepo.repository import Repository

imagerepo_ns = ConfigNamespace("imagerepo", help_section="image repository parameters")
imagerepo_ns.add_parameter(
    "root_manifest",
    advanced=True,
    default="http://support.brightcomputing.com/imagerepo/repo.yaml",
    help_varname="URL",
    help="URL to the image repository yaml manifest"
)


class RepoImageSource(ImageSource):
    def __init__(self, root_manifest=None, **kwargs):
        super().__init__(**kwargs)
        self.root_manifest = root_manifest
        assert not self.uuids

    @classmethod
    def from_config(cls, config, ids=None):
        assert ids is None
        return RepoImageSource(
            ids=config["ids"],
            root_manifest=config["root_manifest"],
            tags=config["tags"],
            version=config["version"],
            distro=config["distro"],
            package_groups=config["package_groups"],
            revision=config["revision"],
            status=config["status"],
            advanced=config["advanced"],
            image_visibility=config["image_visibility"],
            cloud_type=config["cloud_type"],
        )

    def _iter_from_source(self):
        repo = Repository.make_from_url(self.root_manifest)
        images = repo.images_rec_noraise()
        return (
            make_cod_image_from_repo(image)
            for image in images
        )


def repo_image_name(image):
    image_type = image.image_type()
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
    return "{0}-{1}-{2}".format(
        prefix,
        image.id(),
        image.revision()
    )


def make_cod_image_from_repo(image):
    # Remove everything after first digit
    # Same logic as in build-cod-image.sh
    distro_family = re.sub(r"\d.*", "", image.os())

    cod_image = CODImage(
        bcm_optional_info=None,
        cloud_type=image.cloud_type(),
        cmd_revision=image.cmd_revision(),
        created_at=datetime.fromtimestamp(image.created_at(), pytz.utc),
        distro=image.os(),
        distro_family=distro_family,
        id=image.id(),
        name=repo_image_name(image),
        image_visibility="public",
        revision=image.revision(),
        size=image.size(),
        tags=image.tags(),
        type=image.image_type(),
        uploaded_at=None,
        uuid="N/A",
        version=str(image.bcm_version()),
        package_groups=sorted(image.package_groups()),
    )
    cod_image.repo_image = image
    return cod_image
