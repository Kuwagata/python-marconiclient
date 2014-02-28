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
"""Implements a message controller that understands Marconi messages."""

from marconiclient.queues.v1 import core


class Message(object):
    """A handler for Marconi server Message resources.
    Attributes are only downloaded once - at creation time.
    """
    def __init__(self, queue, href, ttl, age, body):
        self.queue = queue
        self.href = href
        self.ttl = ttl
        self.age = age
        self.body = body

        # NOTE(flaper87): Is this really
        # necessary? Should this be returned
        # by Marconi?
        self._id = href.split('/')[-1]

    def __repr__(self):
        return '<Message id:{id} ttl:{ttl}>'.format(id=self._id,
                                                    ttl=self.ttl)

    def delete(self):
        req, trans = self.queue.client._request_and_transport()
        core.message_delete(trans, req, self.queue._name, self._id)
