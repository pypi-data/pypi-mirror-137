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

from six.moves import map

from ..parser_utils import parser_for_type
from .parameter_creation_validation import type_of_value


def complete_env(parameter):
    if parameter.env is None:
        parameter.env = "COD_" + parameter.name.upper()


def complete_flags(parameter):
    parameter.flags = [flag for flag in parameter.flags if flag != parameter.default_flag]


def complete_help_text(parameter):
    if not parameter.help:
        return

    parameter.help = parameter.help.strip()
    if "." != parameter.help[-1]:
        parameter.help += "."


def complete_help_varname_from_name(parameter):
    if parameter.help_varname is None:
        parameter.help_varname = parameter.name.upper()


def complete_help_varname_from_type(parameter):
    if not parameter.help_varname:
        if parameter.type is bool:
            parameter.help_varname = "{TRUE,FALSE}"
        elif parameter.type is int:
            parameter.help_varname = "NUMBER"


def complete_help_varname_from_choices(parameter):
    if not parameter.help_varname and parameter.choices:
        parameter.help_varname = "{%s}" % (", ".join(map(str, parameter.choices)))


def complete_key(parameter):
    if not parameter.key:
        parameter.key = parameter.name


def complete_type_from_default_value(parameter):
    if parameter.type:
        return
    elif parameter.default is not None and parameter.default != [] and not callable(parameter.default):
        parameter.type = type_of_value(parameter.default)


def complete_single_value_type_from_choices(parameter):
    if parameter.type or not parameter.choices:
        return
    parameter.type = type_of_value(parameter.choices)[0]


def complete_list_value_type_from_choices(parameter):
    if parameter.type or not parameter.choices:
        return
    parameter.type = type_of_value(parameter.choices)


def complete_parser_from_type(parameter):
    if parameter.parser:
        return
    elif isinstance(parameter.type, list):
        parameter.parser = parser_for_type(parameter.type[0])
    else:
        parameter.parser = parser_for_type(parameter.type)
