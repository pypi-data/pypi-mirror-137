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


class NodeDefinition(object):
    """Definition of a set of nodes with the same flavor/ set of volumes and prefix."""

    def __init__(self, count, flavor, boot_image=None, root_image=None,
                 disks=None, availability_zone=None, prefix="node"):
        if disks is None:
            disks = []

        self.count = int(count)
        self.flavor = flavor
        self.boot_image = boot_image
        self.root_image = root_image
        self.prefix = prefix
        self.disks = disks
        self.names = ["%s%03d" % (self.prefix, x) for x in range(1, self.count + 1)]
        self.availability_zone = availability_zone

    def __str__(self):
        obj = self.generate_definition()
        obj.update(class_name=self.__class__.__name__)

        return ("<{class_name} count={count}, "
                "flavor='{flavor}', "
                "boot_image='{boot_image}', "
                "root_image='{root_image}', "
                "prefix='{prefix}', disks={disks}, "
                "names={names}, "
                "availability_zone={availability_zone}>"
                .format(**obj))

    def generate_definition(self):
        return {
            "count": self.count,
            "flavor": self.flavor,
            "boot_image": self.boot_image,
            "root_image": self.root_image,
            "prefix": self.prefix,
            "disks": self.disks,
            "names": self.names,
            "availability_zone": self.availability_zone
        }
