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

from abc import ABCMeta, abstractmethod

import six


class Configuration(six.with_metaclass(ABCMeta, object)):  # pragma: no cover
    """Shared interface for CommandConfiguration and CollectiveConfiguration."""

    @abstractmethod
    def __init__(self, parameters):
        pass

    @abstractmethod
    def view_for_namespace(self, namespace):
        pass

    @abstractmethod
    def set_value(self, parameter, value, source):
        pass

    @abstractmethod
    def set_locked_value(self, parameter, value, source):
        pass

    @abstractmethod
    def is_value_locked_for_parameter(self, parameter):
        pass

    @abstractmethod
    def get_parameter_value(self, parameter):
        pass

    @abstractmethod
    def get_source_of_parameter_value(self, parameter):
        pass

    @abstractmethod
    def reduced_dict(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass
