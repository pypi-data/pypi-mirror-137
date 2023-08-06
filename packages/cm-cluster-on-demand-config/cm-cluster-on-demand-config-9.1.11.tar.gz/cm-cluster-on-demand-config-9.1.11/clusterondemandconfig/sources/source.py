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


class Source(six.with_metaclass(ABCMeta, object)):
    """Abstract superclass that specifies all public methods that a Source must implement."""

    @abstractmethod
    def has_value_for_parameter(self, parameter, configuration):  # pragma: no cover
        pass

    @abstractmethod
    def is_enforcing(self):
        pass

    @abstractmethod
    def get_value_for_parameter(self, parameter, configuration):  # pragma: no cover
        pass

    def get_location_of_parameter_value(self, parameter):
        return str(self)

    def __eq__(self, other):  # pragma: no cover
        return type(self) == type(other) and self.__dict__ == other.__dict__

    def __ne__(self, other):  # pragma: no cover
        return not self == other
