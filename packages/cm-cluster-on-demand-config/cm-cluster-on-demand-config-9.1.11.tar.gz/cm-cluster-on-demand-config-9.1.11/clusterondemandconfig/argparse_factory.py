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

import argparse

from clusterondemandconfig.parameter import (
    EnumerationParameter,
    PositionalParameter,
    RepeatingPositionalParameter,
    SimplePositionalParameter,
    SwitchParameter
)


def argparse_parser_for_command_context(command_context):
    parser = argparse.ArgumentParser(
        description="Cluster-on-demand by Bright Computing",
        argument_default=argparse.SUPPRESS
    )
    # TODO: These are toplevel parameters, perhaps put them in command_context somehow?
    parser.add_argument("--config", "-c")
    parser.add_argument("--no-system-config", action="store_true")
    parser.add_argument("-v", "-vv", "-vvv", action="store_true")
    parser.add_argument("--show-configuration", action="store_true")
    parser.add_argument("--log-file")
    parser.add_argument("--version", action="store_true")

    group_parsers = parser.add_subparsers(dest="group")
    group_parsers.required = True
    for command_group in command_context:
        _add_parser_for_command_group(group_parsers, command_group)

    return parser


def _add_parser_for_command_group(group_parsers, group):
    group_parser = group_parsers.add_parser(group.name, aliases=group.aliases, help=group.help)
    command_parsers = group_parser.add_subparsers(dest="command")
    command_parsers.required = True
    for command in group.commands:
        _add_parser_for_command(group_parsers, command_parsers, command)


def _add_parser_for_command(group_parsers, command_parsers, command):
    combined_name = command.group.name + " " + command.name

    if command.combined_aliases:
        group_parsers.add_parser(combined_name, aliases=command.combined_aliases, help=command.help, add_help=False)
    command_parsers.add_parser(command.name, aliases=command.aliases, help=command.help, add_help=False)


def argparse_parser_for_parameters(parameters):
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS, add_help=False)
    for parameter in parameters:
        _add_parser_argument_for_parameter(parser, parameter)
    return parser


def _add_parser_argument_for_parameter(parser, parameter):
    if isinstance(parameter, PositionalParameter):
        parser.add_argument(
            parameter.name,
            **_parser_argument_kwargs_for_parameter(parameter)
        )
    elif isinstance(parameter, SwitchParameter):
        parser.add_argument(
            *parameter.all_flags,
            dest=parameter.name,
            action="store_true"
        )
        parser.add_argument(
            parameter.flag_with_prefix("no"),
            dest=parameter.name,
            action="store_false"
        )
    elif isinstance(parameter, EnumerationParameter):
        parameter_kwargs = _parser_argument_kwargs_for_parameter(parameter)
        parser.add_argument(
            *parameter.all_flags,
            dest=parameter.name,
            **parameter_kwargs
        )
        parser.add_argument(
            parameter.flag_with_prefix("prepend"),
            dest="prepend-" + parameter.name,
            **parameter_kwargs
        )
        parser.add_argument(
            parameter.flag_with_prefix("append"),
            dest="append-" + parameter.name,
            **parameter_kwargs
        )
    else:
        parser.add_argument(
            *parameter.all_flags,
            dest=parameter.name,
            **_parser_argument_kwargs_for_parameter(parameter)
        )


def _parser_argument_kwargs_for_parameter(parameter):
    kwargs = {}
    kwargs["type"] = parameter.parser

    if hasattr(parameter, "choices") and parameter.choices:
        kwargs["choices"] = parameter.choices

    if isinstance(parameter, EnumerationParameter):
        kwargs["nargs"] = "*"
        kwargs["action"] = "append"
    if isinstance(parameter, SimplePositionalParameter):
        kwargs["nargs"] = "?"
    if isinstance(parameter, RepeatingPositionalParameter):
        kwargs["nargs"] = "*"

    return kwargs
