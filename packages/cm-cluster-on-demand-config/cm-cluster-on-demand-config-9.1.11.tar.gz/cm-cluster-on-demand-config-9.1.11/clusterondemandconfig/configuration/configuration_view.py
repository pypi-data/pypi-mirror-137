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

from abc import ABCMeta, abstractmethod

import six


class ConfigurationView(six.with_metaclass(ABCMeta, object)):  # pragma: no cover
    """Shared interface for CommandConfiguration, ConfigurationForNamespaceView and GlobalConfiguration."""

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __contains__(self, key):
        pass

    @abstractmethod
    def get_item_for_key(self, key):
        pass

    @abstractmethod
    def __format__(self, format):
        pass

    def get(self, key, default=None):
        return self[key] if key in self else default

    def item_repr(self, key):
        return f"{self.get_item_for_key(key).parameter.default_flag}={self[key]}"
