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

import logging
import time

import six

log = logging.getLogger("cluster-on-demand")


def memoized(fn):
    """A utility decorator that helps simplifying memoizing methods."""
    class context:
        result = None
        called = False

    def wrapper(*args, **kwargs):
        if not context.called:
            context.result = fn(*args, **kwargs)
            context.called = True
        return context.result
    return wrapper


def retry(timeout, only_retry_on_exception=None, wait_between_retries=None):
    """Call the wrapped function multiple times for a limited amount of time.

    This method is similar to retrying.retry. An added feature is that it keeps the wrapped function
    up to date on the amount of attempts tried and how much time is left. Exceptions raised by the
    method are ignored until the timeout has expired, after which the most recent exception is
    reraised. An exception to this exceptional exception handling is when only_retry_on_exception is
    set. In that case, the first exception that does not match with only_retry_on_exception is
    raised, even if the timeout didn't expire.
    """
    if only_retry_on_exception \
       and not isinstance(only_retry_on_exception, (type, str)) \
       and not callable(only_retry_on_exception):
        raise TypeError("only_retry_on_exception must be either None, a type, a str, or callable.")

    def decorator(fn):
        def wrapper(*args, **kwargs):
            start = time.time()
            deadline = start + timeout
            attempts = 0

            while True:
                try:
                    kwargs.update({"attempts": attempts, "time_left": deadline - time.time()})
                    return fn(*args, **kwargs)
                except Exception as e:
                    log.debug("Retry caught exception: " + str(e))
                    if time.time() > deadline:
                        raise
                    elif isinstance(only_retry_on_exception, type) and not isinstance(e, only_retry_on_exception):
                        raise
                    elif isinstance(only_retry_on_exception, str) and not only_retry_on_exception == str(e):
                        raise
                    elif callable(only_retry_on_exception) and not only_retry_on_exception(e):
                        raise
                    else:
                        attempts += 1
                        if wait_between_retries is not None:
                            time.sleep(wait_between_retries)
        return wrapper
    return decorator


def static_vars(**kwargs):
    """Set some local static variables in a function.

    This will be a global variable, but linked to a function by being an attribute of it

    Example:
    @static_vars(my_var=0):
    def f():
      f.my_var += 1
    """
    def decorator(func):
        for key, value in six.iteritems(kwargs):
            setattr(func, key, value)
        return func
    return decorator
