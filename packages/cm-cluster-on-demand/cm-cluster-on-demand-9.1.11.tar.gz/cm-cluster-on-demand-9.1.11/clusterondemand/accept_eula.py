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

import logging
import os
import sys
import textwrap

from six.moves import input

PATH_TO_CURRENT_EULA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "license-bright-rhel.txt")

EULA_DIALOG_TEXT = ("""
Before this setup can continue, the End-User License Agreement for Bright CM must be read and
accepted. It can be found at:
  %s

Please exit this program with Ctrl+C and read the terms within this file. If this has already been
done, continue by typing 'accept' and pressing enter.

Once accepted, this dialog will not be shown again until a newer version of the EULA becomes available.
""" % (PATH_TO_CURRENT_EULA)).strip()

CANNOT_PROMPT_ACCEPT_ERROR = ("""
Cannot continue with this setup until the EULA has been accepted.

Either run this program with the flag --accept-eula, set the environment variable COD_ACCEPT_EULA=True,
or store the following in a cluster-on-demand config file:

----
[common.eula]
accept_eula=True
----
""")

log = logging.getLogger("cluster-on-demand")


def user_accepts_eula(configuration):
    """Return True when the user accepts, or previously accepted, the current EULA.

    When the user accepts the EULA, a copy of the text is written to a certain file
    (config["user_accepted_eula_file"]). As long as the contents of that file are identical to the
    contents of PATH_TO_CURRENT_EULA, we don't ask the user to accept the EULA again.
    """
    current_eula = _contents_of_file(PATH_TO_CURRENT_EULA)

    if _user_previously_accepted_current_eula(configuration, current_eula):
        return True
    elif _user_accepts_current_eula(configuration):
        _save_current_eula(configuration, current_eula)
        return True
    else:
        return False


def _user_previously_accepted_current_eula(configuration, current_eula):
    return os.path.exists(configuration["user_accepted_eula_file"]) and \
        _contents_of_file(configuration["user_accepted_eula_file"]) == current_eula


def _contents_of_file(path):
    with open(path, "r") as f:
        return f.read()


def _save_current_eula(configuration, current_eula):
    with open(configuration["user_accepted_eula_file"], "w") as f:
        f.write(current_eula)


def _user_accepts_current_eula(configuration):
    if configuration["accept_eula"]:
        log.debug("User accepted the EULA through the configuration.")
        return True

    if not sys.stdout.isatty():
        raise RuntimeError(CANNOT_PROMPT_ACCEPT_ERROR)

    print(textwrap.dedent(EULA_DIALOG_TEXT))

    while True:
        try:
            if _prompt_user_for_accept():
                print("The EULA was accepted. A copy is stored in %s" % (configuration["user_accepted_eula_file"]))
                return True
            else:
                print("Please either type 'accept' and press Enter, or exit with Ctrl+C")
        except KeyboardInterrupt:
            log.debug("User did not accept EULA, sent Ctrl+C instead")
            return False


def _prompt_user_for_accept():
    return "accept" == input()
