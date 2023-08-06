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

from clusterondemandconfig.argparse_factory import argparse_parser_for_parameters
from clusterondemandconfig.exceptions import UnknownCLIArgumentError
from clusterondemandconfig.parameter import EnumerationParameter

from .source import Source


class CLISource(Source):
    """Parameter value source for the config loader that obtains values from sys.argv."""

    def __init__(self, parameters, strict):
        parser = argparse_parser_for_parameters(parameters)
        self.parsed, unknown = parser.parse_known_args()
        if strict and unknown:
            raise UnknownCLIArgumentError(unknown)

    def is_enforcing(self):
        return False

    def __str__(self):  # pragma: no cover
        return "cli"

    def has_value_for_parameter(self, parameter, configuration):
        if self._has_value(parameter.name):
            return True
        elif isinstance(parameter, EnumerationParameter):
            return self._has_value("prepend-" + parameter.name) or self._has_value("append-" + parameter.name)
        else:
            return False

    def get_value_for_parameter(self, parameter, configuration):
        assert self.has_value_for_parameter(parameter, configuration)

        if isinstance(parameter, EnumerationParameter):
            current_value = configuration[parameter.key] if parameter.key in configuration else None
            return self._value_for_enum_parameter(parameter, current_value)
        else:
            return self._get_value(parameter.name)

    def _value_for_enum_parameter(self, parameter, previous_value):
        if self._has_value(parameter.name):
            center = self._get_enum_value(parameter.name)
        else:
            center = previous_value or []
        prepend = self._get_enum_value("prepend-" + parameter.name)
        append = self._get_enum_value("append-" + parameter.name)
        return prepend + center + append

    def _has_value(self, name):
        return hasattr(self.parsed, name)

    def _get_enum_value(self, name):
        return [item for group in self._get_value(name, []) for item in group]

    def _get_value(self, name, *args):
        return getattr(self.parsed, name, *args)
