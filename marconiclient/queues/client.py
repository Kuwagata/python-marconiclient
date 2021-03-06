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

from marconiclient import errors
from marconiclient.queues.v1 import client as cv1

_CLIENTS = {1: cv1.Client}


def Client(url=None, version=None, conf=None):
    try:
        return _CLIENTS[version](url, version, conf)
    except KeyError:
        raise errors.MarconiError('Unknown client version')
