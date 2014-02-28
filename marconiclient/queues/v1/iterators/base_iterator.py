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

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class _Iterator(object):

    def __init__(self, client, listing_response):
        self._client = client

        self._links = []
        self._listing_response = listing_response

    def __iter__(self):
        return self

    @abc.abstractmethod
    def create_object(self, args):
        pass

    @abc.abstractmethod
    def get_iterables(self, iterables):
        pass

    def _next_page(self):
        for link in self._links:
            if link['rel'] == 'next':
                iterables = self._client.follow(link['href'])

                if iterables:
                    self.get_iterables(iterables)
                    return
        raise StopIteration

    def __next__(self):
        try:
            args = self._listing_response.pop(0)
        except IndexError:
            self._next_page()
            return self.next()
        return self.create_object(args)

    next = __next__
