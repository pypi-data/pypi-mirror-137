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

import importlib

import six


def import_if_exists(module):
    """Try to import a module. If the module does not exist, nothing is raised."""
    try:
        return importlib.import_module(module)
    except ImportError as error:
        possible_error_messages = ["No module named %s" % (fragment) for fragment in _module_path_fragments(module)]

        if str(error) in possible_error_messages:
            return None
        else:
            raise


def load_module_attribute(module_path, attribute):
    """Return the value of `module_path`.`attribute`, None if the module is not available."""
    module = import_if_exists(module_path)
    return eval("module.%s" % (attribute)) if module else None


if six.PY2:
    def _module_path_fragments(module_path):
        """Convert a module path like 'foo.bar.baz' to ['foo.bar.baz', 'bar.baz', 'baz']."""
        fragments = []
        while "." in module_path:
            fragments.append(module_path)
            module_path = module_path[module_path.index(".") + 1:]
        return fragments + [module_path]
elif six.PY3:
    def _module_path_fragments(module_path):
        """Convert a module path like 'foo.bar.baz' to ["'foo'", "'foo.bar'", "'foo.bar.baz'"]."""
        fragments = []
        while "." in module_path:
            fragments.append("'%s'" % (module_path))
            module_path = module_path[:module_path.index(".")]
        return fragments + ["'%s'" % (module_path)]
