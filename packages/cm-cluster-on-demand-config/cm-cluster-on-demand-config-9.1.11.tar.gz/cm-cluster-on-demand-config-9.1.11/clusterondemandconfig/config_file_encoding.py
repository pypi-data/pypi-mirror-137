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

# String values that begin or end with whitespace characters are wrapped in one these characters to
# prevent ConfigParser from removing the whitespace characters.
QUOTE_SYMBOLS = ('"', "'")


def encode(parameter, value):
    if value is None:
        return "None"
    elif isinstance(parameter.type, list):
        return ",".join(map(parameter.serializer, value))
    else:
        value = parameter.serializer(value)
        if parameter.type == str:
            value = _wrap_in_symbols(value)
        return value


def _wrap_in_symbols(string):
    if len(string) == 0:
        return '""'
    elif string != string.strip():
        return '"%s"' % string.replace('"', '\\"')
    else:
        return string


def remove_any_wrapping_symbols(string):
    for symbol in QUOTE_SYMBOLS:
        if string.startswith(symbol) and string.endswith(symbol):
            return string.strip(symbol).replace("\\" + symbol, symbol)
    return string
