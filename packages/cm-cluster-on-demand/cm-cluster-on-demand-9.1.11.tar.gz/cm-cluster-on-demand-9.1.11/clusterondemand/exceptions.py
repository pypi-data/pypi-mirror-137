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

import traceback


class CODException(Exception):
    """Exceptions raised inside COD with some useful user readable message

    :param caused_by: If the exception was raised inside some except block
        the original exception can be specified here for better logging later
    """
    def __init__(self, message, caused_by=None):
        super(CODException, self).__init__(message)
        self.caused_by = caused_by
        self.caused_by_trace = traceback.format_exc()


class UserReportableException(CODException):
    """Exception class reserved for customer portal error messages."""

    pass


class ValidationException(UserReportableException):
    """Exception class reserved for errors validating parameters.

    All validations errors should be shown to the user, so this type extends UserReportableException
    """

    pass
