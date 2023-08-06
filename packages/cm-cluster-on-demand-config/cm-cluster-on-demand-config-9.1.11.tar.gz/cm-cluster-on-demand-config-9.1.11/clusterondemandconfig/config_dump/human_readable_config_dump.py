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

import six
from prettytable import PrettyTable

# The maximum width of the option or value column. If the value is too long, then it is wrapped to
# the next line.
MAX_WIDTH_COLUMN = 120


def human_readable_config_dump(config, show_secrets):
    """Shows the configuration. For each item, the option namespace, value and source of the value are reported.

    The value column is supposed to be limited to MAX_LENGTH_VALUE_COLUMN characters, but if the path
    of a source file is too long, the column can become wider than that. In that case, the printer
    tries to print the source on a separate line.
    """
    table = PrettyTable()
    for name in ["option", "value"]:
        table.add_column(name, [], align="l")
    table._set_max_width(MAX_WIDTH_COLUMN)

    for (unique_name, item) in six.iteritems(config.reduced_dict()):
        location = item.source.get_location_of_parameter_value(item.parameter)

        if item.value and item.parameter.secret and not show_secrets:
            value = "X" * 15
            comment = "# use '--show-secrets' to uncover"
        else:
            value = _human_readable_value(item.parameter, item.value)
            comment = ""

        table.add_row([unique_name, "%s (%s)  %s" % (value, location, comment)])

    return table.get_string(sortby="option")


def _human_readable_value(parameter, value):
    if isinstance(parameter.type, list):
        return _serialize_list_value(parameter.serializer, value)
    else:
        return _serialize_single_value(parameter.serializer, value)


def _serialize_single_value(serializer, value):
    if value is None:
        return "None"
    elif type(value) in [bool, int, str]:
        return repr(value)
    else:
        return repr(serializer(value))


def _serialize_list_value(serializer, values):
    if values is None:
        return "None"
    else:
        return "[%s]" % (",".join(_serialize_single_value(serializer, value) for value in values))
