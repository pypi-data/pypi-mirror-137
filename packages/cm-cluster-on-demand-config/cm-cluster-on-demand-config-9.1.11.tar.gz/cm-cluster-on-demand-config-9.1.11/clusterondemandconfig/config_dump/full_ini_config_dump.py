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

import collections
import sys
import textwrap
from contextlib import contextmanager

from six import StringIO

from clusterondemandconfig.config_file_encoding import encode
from clusterondemandconfig.configuration import CollectiveConfiguration, CommandConfiguration
from clusterondemandconfig.parameter import EnumerationParameter, PositionalParameter, SimpleParameter

MAX_WIDTH = 80


def full_ini_config_dump(config_to_dump, show_secrets):
    """Generates an ini file that contains the entire configuration.

    To help the user with maintaining such an ini file, each item is preceded by the help text.
    """

    config_items = [
        item for item in config_to_dump.reduced_dict().values()
        if not isinstance(item.parameter, PositionalParameter)
    ]
    parameters = map(lambda item: item.parameter, config_items)

    if isinstance(config_to_dump, CommandConfiguration):
        groups = _group_config_items(config_items, key=lambda item: item.parameter.namespaces[0])
    elif isinstance(config_to_dump, CollectiveConfiguration):
        groups = _group_config_items(config_items, key=lambda item: item.parameter.namespace.name)
    else:
        assert False  # pragma: no cover

    buffer = StringIO()
    with _capture_stdout(buffer):
        for namespace in sorted(_parameter_namespaces(parameters), key=lambda ns: ns.name):
            _print_section_title(namespace)
            for item in sorted(groups[namespace.name], key=lambda item: item.parameter.name):
                if item.parameter.secret and not show_secrets:
                    continue

                _print_help(item.parameter)
                _print_assignment(item.parameter, item.value)
                _print_newline()
            _print_newline()

    return buffer.getvalue()


@contextmanager
def _capture_stdout(buffer):
    sys.stdout, old_stdout = buffer, sys.stdout
    try:
        yield
    finally:
        sys.stdout = old_stdout


def _group_config_items(config_items, key):
    groups = collections.defaultdict(lambda: [])

    for config_item in config_items:
        groups[key(config_item)].append(config_item)

    return groups


def _parameter_namespaces(parameters):
    namespaces = {}

    for parameter in parameters:
        while parameter:
            namespaces[parameter.namespace.name] = parameter.namespace
            parameter = parameter.parent

    return namespaces.values()


def _print_section_title(namespace):
    print("[%s]" % (namespace.name))


def _print_assignment(parameter, value):
    encoded_value = encode(parameter, value)

    if "\n" not in encoded_value:
        print("%s = %s" % (parameter.name, encoded_value))
    else:
        lines = ("%s = %s" % (parameter.name, encoded_value)).split("\n")
        print(lines[0])
        for line in lines[1:]:
            print("  %s" % (line))


def _print_help(parameter):
    _print_wrapped_comment("%s" % (parameter.help))
    if isinstance(parameter, SimpleParameter) and parameter.choices:
        _print_wrapped_comment("Value is one of: %s." % _encode_choices(parameter, parameter.choices))
    elif isinstance(parameter, EnumerationParameter) and parameter.choices:
        _print_wrapped_comment("Value may contain one or more of: %s." % _encode_choices(parameter, parameter.choices))


def _print_wrapped_comment(comment):
    if len(comment) < MAX_WIDTH:
        print("# %s" % (comment))
    else:
        lines = textwrap.wrap(comment, width=MAX_WIDTH - len("#  "))

        print("# %s" % (lines[0]))
        for line in lines[1:]:
            print("#  %s" % (line))


def _print_newline():
    print("")


def _encode_choices(parameter, choices):
    fragments = []

    for choice in sorted(choices):
        encoded_value = parameter.serializer(choice)
        if parameter.help_choices and choice in parameter.help_choices:
            fragments.append("%s - %s" % (encoded_value, parameter.help_choices[choice]))
        else:
            fragments.append(encoded_value)

    return "; ".join(fragments)
