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

from .source import Source


class DynamicDefaultSource(Source):
    """Parameter value source that fills the configuration with the default value if that value is dynamic.

    A dynamic default is callable and calling it will produce the actual default value.
    """

    def __str__(self):  # pragma: no cover
        return "default"

    def is_enforcing(self):
        return False

    def has_value_for_parameter(self, parameter, configuration):
        return configuration.get_source_of_parameter_value(parameter) is None \
            and callable(parameter.default)

    def get_value_for_parameter(self, parameter, configuration):
        assert self.has_value_for_parameter(parameter, configuration)

        return parameter.default(parameter, configuration.view_for_namespace(parameter.namespace))
