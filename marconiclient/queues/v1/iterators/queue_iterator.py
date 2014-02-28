# Copyright (c) 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from marconiclient.queues.v1.iterators import base_iterator
from marconiclient.queues.v1 import queues


class _QueueIterator(base_iterator._Iterator):
    """Queue Iterator

    This iterator is not meant to be used outside
    the scope of this package. The iterator gets
    a dictionary as returned by the queue listing
    endpoint and iterates over the messages in the
    `queues` key.

    If there are no queues left to return, the iterator
    will try to load more by following the `next` rel link
    type.

    The iterator raises a StopIteration exception if the server
    doesn't return more queues after a `next-page` call.

    :param client: The client instance
    :type client: `v1.Client`
    :param listing_response: Response returned by the listing call
    :type listing_response: Dict
    """

    def __init__(self, client, listing_response):
        self._client = client

        self._links = listing_response['links']
        self._listing_response = listing_response['queues']

    def create_object(self, args):
        return queues.Queue(self._client, args["name"], False)

    def get_iterables(self, iterables):
        self._links = iterables['links']
        self._listing_response = iterables['queues']