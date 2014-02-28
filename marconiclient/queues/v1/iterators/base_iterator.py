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
    """Base Iterator

    This iterator is not meant to be used outside
    the scope of this package. The iterator gets
    a dictionary as returned by a listing endpoint.
    
    Subclasses of this base class determine the key
    to iterate over, as well as the means of creating
    the objects contained within.

    If there are no objects left to return, the iterator
    will try to load more by following the `next` rel link
    type.

    The iterator raises a StopIteration exception if the server
    doesn't return more objects after a `next-page` call.

    :param client: The client instance used by the queue
    :type client: `v1.Client`
    :param listing_response: Response returned by the listing call
    :type listing_response: Dict
    """
    def __init__(self, client, listing_response):
        self._client = client

        self._links = []
        self._listing_response = listing_response

    def __iter__(self):
        return self

    @abc.abstractmethod
    def create_object(self, args):
        """Must be subclassed
        
        :param args: Args used for object creation
        :type listing_response: Dict
        """

    @abc.abstractmethod
    def get_iterables(self, iterables):
        """Must be subclassed to determine key to iterate over
        
        :param iterables: Dictionary to iterate over
        :type iterables: Dict
        """

    def _next_page(self):
        for link in self._links:
            if link['rel'] == 'next':
                # NOTE(flaper87): We already have the
                # ref for the next set of messages, lets
                # just follow it.
                iterables = self._client.follow(link['href'])

                # NOTE(flaper87): Since we're using
                # `.follow`, the empty result will
                # be None. Consider making the API
                # return an empty dict for consistency.
                if iterables:
                    # NOTE(Kuwagata): Child class determines
                    # the key to iterate over.
                    self.get_iterables(iterables)
                    return
        raise StopIteration

    def __next__(self):
        try:
            args = self._listing_response.pop(0)
        except IndexError:
            self._next_page()
            return self.next()
        # NOTE(Kuwagata): Object creation is deferred to the
        # child classes.
        return self.create_object(args)

    # NOTE(flaper87): Py2K support
    next = __next__
