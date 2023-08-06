from six.moves import map

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


class BcmVersion(object):
    """A utility class for comparing Bright Cluster Manager versions.

    Wraps a version number string and handles comparison logic. The string cannot contain a revision
    suffix, yet.

    Hard-coded assumption: At Bright, once we start working on BCM with major version X, then we
    will never release another minor version of a major X-1. That is: there will never be a release
    of something like 8.4 if 9.0 has been released (even internally).

    Also, it doesn't consider the tag after the dash (i.e: 8.1-2). This can be implemented in future if
    we see it as necessary
    """

    @classmethod
    def _wrap_with_instance(self, obj):
        return obj if isinstance(obj, self) else self(obj)

    def __init__(self, string):

        self.string = string
        self.is_trunk, self.major, self.minor = None, None, None

        if "trunk" == string:
            self.is_trunk = True
        else:
            major_dot_minor = string.split("-")[0]
            self.major, self.minor = map(int, major_dot_minor.split("."))

    def __str__(self):
        return self.string

    def __eq__(self, other):
        other = self.__class__._wrap_with_instance(other)
        return (
            self.is_trunk == other.is_trunk and
            self.major == other.major and
            self.minor == other.minor
        )

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        other = self.__class__._wrap_with_instance(other)
        if self.is_trunk:
            return not other.is_trunk
        elif other.is_trunk:
            return False
        else:
            return self.major > other.major or \
                (self.major == other.major and self.minor > other.minor)

    def __ge__(self, other):
        return self == other or self > other

    def __lt__(self, other):
        return not self >= other

    def __le__(self, other):
        return not self > other
