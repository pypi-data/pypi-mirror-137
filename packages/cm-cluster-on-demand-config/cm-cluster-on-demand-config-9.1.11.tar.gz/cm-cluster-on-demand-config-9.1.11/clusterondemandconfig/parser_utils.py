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

import re

from six.moves import map

from .exceptions import ConfigLoadError


def parser_for_type(type):
    return boolean_parser if type is bool else type


def boolean_parser(string):
    """Parse string to boolean value."""
    YES = ["y", "on", "yes", "true", "1"]
    NO = ["n", "no", "off", "false", "0"]
    if string.lower() in YES:
        return True
    elif string.lower() in NO:
        return False
    else:
        raise ConfigLoadError("Expected %s for yes or %s for no. Got '%s'." % (",".join(YES), ",".join(NO), string))


def parse_single_value(parameter, value):
    if value.strip() == "None":
        return None
    else:
        parsed_value = parameter.parser(value)

        if hasattr(parameter, "choices") and parameter.choices:
            _raise_if_not_in_choices(parsed_value, parameter.choices)

        return parsed_value


def parse_multiple_values(parameter, value):
    if not value:
        return []
    elif value.strip() == "None":
        return None
    parsed_values = [parameter.parser(v.strip()) for v in re.split(",\n?", value)]

    if hasattr(parameter, "choices") and parameter.choices:
        for parsed_value in parsed_values:
            _raise_if_not_in_choices(parsed_value, parameter.choices)

    return parsed_values


def _raise_if_not_in_choices(value, choices):
    if value not in choices:
        raise ConfigLoadError("%s is not a valid value. Valid values are {%s}" %
                              (value, ",".join(map(str, choices))))
