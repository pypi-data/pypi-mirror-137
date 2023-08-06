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
import random
import time

from azure.core.exceptions import HttpResponseError

log = logging.getLogger("azure_action")


def randomize_upper_limit(number, normalized_amount):
    """Return a random number within a range.

    [number - (number * normalized_amout); number + (number * normalized_amount)]
    """
    lower_bound = number - (number * normalized_amount)
    upper_bound = number + (number * normalized_amount)
    return random.uniform(lower_bound, upper_bound)


def randomized_exp_backoffs(max_iterations):
    """Return a generator for randomized exponential backoffs."""
    iteration = 1
    while iteration <= max_iterations:
        backoff_sec = pow(2, iteration)
        randomized_sec = randomize_upper_limit(backoff_sec, 0.3)
        iteration += 1
        yield randomized_sec


class RetryLimitReached(Exception):
    pass


def unthrottle(fun, backoffs):
    """Will call fun and return it's value unless an exception is thrown.

    If exception is thrown, will call the function again based on the
    back-offs.
    """
    for backoff_time in backoffs:
        try:
            return fun()
        except HttpResponseError as e:
            if e.status_code == 429:
                log.debug("Caught a throttling http code, will retry...")
                time.sleep(backoff_time)
            else:
                raise

    raise RetryLimitReached("Reached limit of retries")


def unt(fun, *args, **kwargs):
    """Easy-to use domain-specific unthrottling wrapper aroung the unthrottle function.

    Use cases:
    1) simple call that returns immediate result
      unt(compute_mgmt_client.virtual_machines.start, resource_group_name, hostname)
    2) call that requires lambda, because the .result() might also throw a throttling exception
      unt(lambda: compute_mgmt_client.virtual_machines.delete(resource_group_name,
                                                              hostname).result())

    """
    return unthrottle(lambda: fun(*args, **kwargs),
                      randomized_exp_backoffs(11))
