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

from clusterondemand.exceptions import CODException
from clusterondemandconfig import ConfigNamespace, config

clusterprefix_ns = ConfigNamespace("cluster.prefix", help_section="Cluster name prefix")
clusterprefix_ns.add_parameter(
    "cod_prefix",
    advanced=True,
    env="COD_PREFIX",
    help="A prefix that is by default prepended to the cluster name when creating a new cluster"
)
clusterprefix_ns.add_switch_parameter(
    "require_cod_prefix",
    advanced=True,
    help=("Whether the tool should require prefix to be set. "
          "The default of this value is typically configured by the cloud-admin.")
)
clusterprefix_ns.add_switch_parameter(
    "enforce_lowercase_cod_prefix",
    advanced=True,
    help="Whether the prefix may only consist of lowercase characters."
)


def get_prefix(config=config):
    prefix = config["cod_prefix"]
    required = config["require_cod_prefix"]
    lowercase = config["enforce_lowercase_cod_prefix"]

    if not prefix and required:
        raise CODException("Please set COD_PREFIX in your environment.")
    elif not prefix:
        return ""
    elif lowercase and not (prefix.isalpha() and prefix.islower()):
        raise CODException("COD_PREFIX may only consist of lowercase alphabetic characters.")

    return prefix


def ensure_cod_prefix(name):
    """Prefix name with COD_PREFIX if needed.

    'name' may contain the prefix already, then 'name' is returned
    If 'name' is None, None is returned. This is useful in the case of an optional parameter
    """
    if name is None:
        return None

    return _ensure_string_starts_with_cod_prefix(name, get_prefix(config))


def must_start_with_cod_prefix(parameter, config):
    """A config validation that will ensure that the parameter value starts with cod_prefix."""
    cod_prefix = get_prefix(config)

    if parameter.type not in [str, [str]]:
        # TODO: CM-20585, handle this statically.
        raise CODException("This validation cannot be used with a parameter of type %s" % (parameter.type.__name__))

    if not cod_prefix or config[parameter.key] is None:
        return
    elif str == parameter.type:
        config[parameter.key] = _ensure_string_starts_with_cod_prefix(config[parameter.key], cod_prefix)
    elif [str] == parameter.type:
        config[parameter.key] = [
            _ensure_string_starts_with_cod_prefix(name, cod_prefix)
            for name in config[parameter.key]
        ]
    else:
        assert False


def _ensure_string_starts_with_cod_prefix(string, cod_prefix):
    if cod_prefix and not string.startswith(cod_prefix + "-"):
        return cod_prefix + "-" + string
    return string
