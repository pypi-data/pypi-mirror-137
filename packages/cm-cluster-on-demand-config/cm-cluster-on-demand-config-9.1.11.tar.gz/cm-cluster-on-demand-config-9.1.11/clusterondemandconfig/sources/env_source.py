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

import os

from clusterondemandconfig.exceptions import ConfigLoadError
from clusterondemandconfig.parameter import EnumerationParameter, PositionalParameter
from clusterondemandconfig.parser_utils import parse_multiple_values, parse_single_value

from .source import Source


class ENVSource(Source):
    """Parameter value source for the config loader that obtains values from os.environ."""

    def __str__(self):  # pragma: no cover
        return "env"

    def is_enforcing(self):
        return False

    def has_value_for_parameter(self, parameter, configuration):
        if isinstance(parameter, PositionalParameter):
            return False
        else:
            return any([env_var in os.environ for env_var in _env_var_names_for_parameter(parameter)])

    def get_value_for_parameter(self, parameter, configuration):
        assert self.has_value_for_parameter(parameter, configuration)

        try:
            if isinstance(parameter, EnumerationParameter):
                current_value = configuration[parameter.key] or []
                return _value_for_enum_parameter(parameter, current_value)
            else:
                return parse_single_value(parameter, os.environ[parameter.env])
        except Exception as e:
            raise ConfigLoadError(
                "An error occured when parsing the value for parameter '%s' set in %s:\n\t%s" %
                (parameter.name, parameter.env, e)
            )

    def get_location_of_parameter_value(self, parameter):
        env_vars = [env_var for env_var in _env_var_names_for_parameter(parameter) if env_var in os.environ]

        return "env: " + ",".join(env_vars)


def _value_for_enum_parameter(parameter, current_value):
    prepend_var_name = env_var_name_with_prefix(parameter, "PREPEND")
    append_var_name = env_var_name_with_prefix(parameter, "APPEND")

    if parameter.env in os.environ:
        value = parse_multiple_values(parameter, os.environ[parameter.env])
    else:
        value = current_value

    if prepend_var_name in os.environ:
        value = parse_multiple_values(parameter, os.environ[prepend_var_name]) + value

    if append_var_name in os.environ:
        value = value + parse_multiple_values(parameter, os.environ[append_var_name])

    return value


def _env_var_names_for_parameter(parameter):
    if isinstance(parameter, EnumerationParameter):
        return [
            parameter.env,
            env_var_name_with_prefix(parameter, "PREPEND"),
            env_var_name_with_prefix(parameter, "APPEND")
        ]
    else:
        return [parameter.env]


def env_var_name_with_prefix(parameter, prefix):
    if parameter.env.startswith("COD_"):
        return "_".join(["COD", prefix, parameter.env[len("COD_"):]])
    else:
        return "_".join([prefix, parameter.env])
