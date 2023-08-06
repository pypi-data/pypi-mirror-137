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

import re
from typing import List, Sequence

from clusterondemandconfig.parameter import (
    EnumerationParameter,
    OptionalParameter,
    Parameter,
    PositionalParameter,
    SwitchParameter
)


def find_parameters_for_identifier(identifier: str, parameters: Sequence[Parameter]) -> List[Parameter]:
    matcher = _matcher_for_identifier(identifier)
    return [
        parameter for parameter in parameters
        if matcher(parameter)
    ]


def _matcher_for_identifier(identifier):
    if identifier.startswith("-"):
        return lambda p: isinstance(p, OptionalParameter) and (
            _parameter_has_flag(p, identifier) or _parameter_has_modifying_flag(p, identifier)
        )
    elif identifier == identifier.upper():
        return lambda p: not isinstance(p, PositionalParameter) and \
            _parameter_has_environment_variable(p, identifier)
    elif identifier.startswith("re:"):
        regex = re.compile(identifier[len("re:"):])
        return lambda p: _parameter_name_matches_regex(p, regex) or _parameter_full_name_matches_regex(p, regex)
    else:
        identifier = _normalize_hyphens(identifier)
        return lambda p: _parameter_has_name(p, identifier) or _parameter_has_full_name(p, identifier)


def _parameter_has_flag(parameter, identifier):
    return identifier in parameter.all_flags


def _parameter_has_modifying_flag(parameter, identifier):
    if isinstance(parameter, SwitchParameter):
        return f"--no-{parameter.name}" == identifier
    elif isinstance(parameter, EnumerationParameter):
        return \
            f"--append-{parameter.name}" == identifier or \
            f"--prepend-{parameter.name}" == identifier
    else:
        return False


def _parameter_has_name(parameter, identifier):
    return parameter.name == identifier


def _parameter_has_environment_variable(parameter, identifier):
    return parameter.env == identifier


def _parameter_has_full_name(parameter, identifier):
    return identifier in map(lambda ns: f"{ns}:{parameter.name}", parameter.namespaces)


def _parameter_name_matches_regex(parameter, regex):
    return re.match(regex, parameter.name)


def _parameter_full_name_matches_regex(parameter, regex):
    return any(map(lambda ns: re.match(regex, f"{ns}:{parameter.name}"), parameter.namespaces))


def _normalize_hyphens(string):
    return string.replace("-", "_")
