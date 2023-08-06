# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Contains helper waiting methods
"""
import time
POLL_FREQUENCY = 2  # How long to sleep in between
IGNORED_EXCEPTIONS = ()  # exceptions ignored during calls to the method
TIME_OUT = 10


class Wait:
    """
    Unify wait library
    """

    def __init__(self, timeout=TIME_OUT, poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        """
        Unify wait library constuctor

        :param timeout: Max time to wait before timeout
        :type timeout: int, optional
        :param poll_frequency: How often the method should be verified
        :type poll_frequency: int, optional
        :param ignored_exceptions: Ignore exceptions
        :type ignored_exceptions: bool, optional
        """

        self._timeout = timeout
        self._poll = poll_frequency

        if self._poll == 0:
            self._poll = POLL_FREQUENCY

        exceptions = list(IGNORED_EXCEPTIONS)

        if ignored_exceptions is not None:

            try:
                exceptions.extend(iter(ignored_exceptions))

            except TypeError:

                exceptions.append(ignored_exceptions)

        self._ignored_exceptions = tuple(exceptions)

    def until(self, method, message='', *args):
        """
        Waits for method to return TRUE.

        :param method: Pointer to a python method
        :type method: function
        :param message: String message to return if method times out
        :type message: str, optional
        :param args: Additional args to be passed to method
        :type args: args
        :return:
        """

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(*args)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                message += str(getattr(exc, 'stacktrace', None))
                break

            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise Exception(message)

    def until_not(self, method, message='', *args):
        """
        Negate until

        :param method: Pointer to a python method
        :type method: method
        :param message: String message to return if method times out
        :type message: str, optional
        :param args: Additional args to be passed to method
        :type args: args
        :return:
        """

        end_time = time.time() + self._timeout

        while True:
            try:
                value = method(*args)
                if not value:
                    return value
            except self._ignored_exceptions as exc:
                message += str(getattr(exc, 'stacktrace', None))
                break

            time.sleep(self._poll)

            if time.time() > end_time:
                break

        raise Exception(message)

    def until_backoff(self, method, message='', *args):
        """
        Waits until with exponential backoff.

        :param method: Pointer to a python method
        :type method: method
        :param message: String message to return if method times out
        :type message: str, optional
        :param args: Additional args to be passed to method
        :type args: args
        :return:
        """
        end_time = time.time() + self._timeout

        new_poll = self._poll

        while True:
            try:
                value = method(*args)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                message += str(getattr(exc, 'stacktrace', None))
                break

            time.sleep(new_poll)

            new_poll *= 0.02

            if time.time() > end_time:
                break
        raise Exception(message)
