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

    def __init__(self, client, listing_response):
        super(_MessageIterator, self).__init__(client, listing_response)

        if isinstance(listing_response, dict):
            self._links = listing_response['links']
            self._listing_response = listing_response['messages']

        from marconiclient.queues.v1 import queues

        if isinstance(self._client, queues.Queue):
            self._queue = self._client
            self._client = self._queue.client

    def create_object(self, args):
        return message.Message(self._queue, **args)

    def get_iterables(self, iterables):
        self._links = iterables['links']
        self._listing_response = iterables['messages']
