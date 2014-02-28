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
from marconiclient.queues.v1 import message


class _MessageIterator(base_iterator._Iterator):
    """Message Iterator

    This iterator is not meant to be used outside
    the scope of this package. The iterator gets
    a dictionary as returned by the message listing
    endpoint and iterates over the messages in the
    `messages` key.

    If there are no messages left to return, the iterator
    will try to load more by following the `next` rel link
    type.

    The iterator raises a StopIteration exception if the server
    doesn't return more messages after a `next-page` call.

    :param queue: The queue instance
    :type client: `v1.Queue`
    :param listing_response: Response returned by the listing call
    :type listing_response: Dict
    """

    def __init__(self, queue, listing_response):
        self._queue = queue
        super(_MessageIterator, self).__init__(queue.client, listing_response)

        # NOTE(flaper87): Simple hack to
        # re-use the iterator for get_many_messages
        # and message listing.
        if isinstance(listing_response, dict):
            self._links = listing_response['links']
            self._listing_response = listing_response['messages']

    def create_object(self, args):
        return message.Message(self._queue, **args)

    def get_iterables(self, iterables):
        self._links = iterables['links']
        self._listing_response = iterables['messages']
