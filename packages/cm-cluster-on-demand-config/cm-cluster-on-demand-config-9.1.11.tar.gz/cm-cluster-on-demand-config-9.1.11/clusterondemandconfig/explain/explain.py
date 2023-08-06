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

import logging
import os
import textwrap

from mako.template import Template

from clusterondemandconfig.command_context import Command, CommandContext
from clusterondemandconfig.parameter import (
    EnumerationParameter,
    RepeatingPositionalParameter,
    SimpleParameter,
    SimplePositionalParameter,
    SwitchParameter
)
from clusterondemandconfig.sources.env_source import env_var_name_with_prefix

from .find_parameters import find_parameters_for_identifier
from .namespace_tree import generate_namespace_tree

log = logging.getLogger("cluster-on-demand")


def explain_parameter(command: Command, context: CommandContext, identifier: str):
    parameters = find_parameters_for_identifier(identifier, command.parameters)
    for parameter in parameters:
        setattr(parameter, "command", command.cli_expression)

    if 0 == len(parameters):
        log.info("No parameters were found that matched the given identifier.")
        log.info("You can specify a flag, environment variable or regular expression.")
        return

    chosen_parameter, *alternative_parameters = parameters
    related_parameters = _find_all_related_parameters(chosen_parameter, context)
    if alternative_parameters:
        log.info("Multiple parameters matched the identifier. Chosing an arbitrary one to display.")

    if isinstance(chosen_parameter, SimpleParameter):
        _print_simple_parameter_explanation(chosen_parameter, related_parameters, alternative_parameters)
    elif isinstance(chosen_parameter, SwitchParameter):
        _print_switch_parameter_explanation(chosen_parameter, related_parameters, alternative_parameters)
    elif isinstance(chosen_parameter, EnumerationParameter):
        _print_enumeration_parameter_explanation(chosen_parameter, related_parameters, alternative_parameters)
    elif isinstance(chosen_parameter, SimplePositionalParameter):
        _print_simple_positional_parameter_explanation(chosen_parameter, related_parameters, alternative_parameters)
    elif isinstance(chosen_parameter, RepeatingPositionalParameter):
        _print_repeating_positional_parameter_explanation(chosen_parameter, related_parameters, alternative_parameters)


def _find_all_related_parameters(parameter, context):
    related_parameters = []
    for command in context.commands():
        for other in command.parameters:
            if parameter.name == other.name and parameter.namespaces[0] == other.namespaces[0]:
                setattr(other, "command", command.cli_expression)
                related_parameters.append(other)
    return related_parameters


def _print_simple_parameter_explanation(parameter, related_parameters, alternatives):
    example_value = f"<{parameter.type.__name__} value>"

    comments = []
    if parameter.default is not None:
        if not callable(parameter.default):
            comments.append(f"Its default value is {parameter.default}.")
            example_value = parameter.default
        else:
            comments.append(f"Its default value is generated from other configuration parameters.")
    else:
        comments.append(f"It has no default value.")

    if parameter.choices:
        comments.append(f"The value of this parameter can be one of {', '.join(parameter.choices)}")

    _print_parameter_explanation(
        parameter,
        command=f"{parameter.command} {' | '.join(map(lambda flag: f'{flag} <value>', parameter.all_flags))}",
        cli_expressions=map(lambda flag: f"{parameter.command} {flag} {example_value} [..]", parameter.all_flags),
        env_expressions=[
            f"{parameter.env}={example_value} {parameter.command} [..]",
        ],
        config_file_expressions=[
            f"[{parameter.namespaces[0]}]\n{parameter.name}={example_value}",
        ],
        tree=generate_namespace_tree([parameter] + related_parameters),
        alternatives=generate_namespace_tree(alternatives),
        comments=comments,
    )


def _print_switch_parameter_explanation(parameter, related_parameters, alternatives):
    comments = ["It is a switch parameter, possible values are True and False."]
    if parameter.default:
        comments.append(f"Its default value is True. Use --no-{parameter.name} to set it to False.")
    else:
        comments.append(f"Its default value is False. Use --{parameter.name} to set it to True.")

    _print_parameter_explanation(
        parameter,
        command=f"{parameter.command} {' | '.join(parameter.all_flags)}",
        cli_expressions=[
            f"{parameter.command} {' | '.join(parameter.all_flags)} [..]",
            f"{parameter.command} --no-{parameter.name} [..]",
        ],
        env_expressions=[
            f"{parameter.env}=True {parameter.command}",
            f"{parameter.env}=False {parameter.command}",
        ],
        config_file_expressions=[
            f"[{parameter.namespaces[0]}]\n{parameter.name}=True",
            f"[{parameter.namespaces[-1]}]\n{parameter.name}=False"
        ],
        tree=generate_namespace_tree([parameter] + related_parameters),
        alternatives=generate_namespace_tree(alternatives),
        comments=comments,
    )


def _print_enumeration_parameter_explanation(parameter, related_parameters, alternatives):
    value1, value2 = "<value1>", "<value2>"

    comments = ["It is an enumeration parameter; it can take zero, one or multiple values."]
    if parameter.default:
        value1 = parameter.default
        comments.append(f"Its default value is {parameter.default}")
    else:
        comments.append(f"It has no default value.")

    if parameter.choices:
        value1, value2, *_ = parameter.choices
        comments.append(f"The value of this parameter can be any subset of {parameter.choices}")

    cli_expressions = []
    for flag in parameter.all_flags:
        cli_expressions.append(f"{parameter.command} {flag} {value1} {value2} .. [..]'")
        cli_expressions.append(f"{parameter.command} {flag} {value1} {flag} {value2} .. [..]'")
    cli_expressions.append(f"{parameter.command} --prepend-{parameter.name} {value1} .. [..]'")
    cli_expressions.append(f"{parameter.command} --append-{parameter.name} {value1} .. [..]'")

    _print_parameter_explanation(
        parameter,
        command=(
            f"{parameter.command} {' | '.join(map(lambda flag: f'{flag} <value1> <value2> ..', parameter.all_flags))}"
        ),
        cli_expressions=cli_expressions,
        env_expressions=[
            f"{parameter.env}={value1},{value2},... {parameter.command}",
            f"{env_var_name_with_prefix(parameter, 'PREPEND')}={value1},{value2},... {parameter.command}",
            f"{env_var_name_with_prefix(parameter, 'APPEND')}={value1},{value2},... {parameter.command}",
        ],
        config_file_expressions=[
            f"[{parameter.namespaces[0]}]\n{parameter.name}={value1},{value2}",
            f"[{parameter.namespaces[-1]}]\n"
            "# Can append or prepend to values that were defined as default or in an earlier config file\n"
            "#  by using the + operator.\n"
            f"{parameter.name}={parameter.name} + {value1},{value2} + {parameter.name}"
        ],
        tree=generate_namespace_tree([parameter] + related_parameters),
        alternatives=generate_namespace_tree(alternatives),
        comments=comments,
    )


def _print_simple_positional_parameter_explanation(parameter, related_parameters, alternatives):
    comments = [
        "It is a positonal parameter, it can not be set through the environment or in a config file."
    ]

    _print_parameter_explanation(
        parameter,
        command=f"{parameter.command} -- {parameter.name}",
        cli_expressions=[f"{parameter.command} -- {parameter.help_varname}"],
        tree=generate_namespace_tree([parameter] + related_parameters),
        alternatives=generate_namespace_tree(alternatives),
        comments=comments,
    )


def _print_repeating_positional_parameter_explanation(parameter, related_parameters, alternatives):
    comments = [
        "It is a positonal parameter, it can not be set through the environment or in a config file.",
        "Multiple values can be set. These are space separated"
    ]

    _print_parameter_explanation(
        parameter,
        command=f"{parameter.command} -- {parameter.name} [{parameter.name} [...]]",
        cli_expressions=[f"{parameter.command} -- {parameter.help_varname} [{parameter.help_varname} [...]]"],
        tree=generate_namespace_tree([parameter] + related_parameters),
        alternatives=generate_namespace_tree(alternatives),
        comments=comments,
    )


def _print_parameter_explanation(
        parameter, command, cli_expressions=None, env_expressions=None, config_file_expressions=None,
        tree="", alternatives=None, comments=None
):
    cli_expressions = cli_expressions or []
    env_expressions = env_expressions or []
    config_file_expressions = config_file_expressions or []
    alternatives = alternatives or []
    comments = comments or []

    with open(os.path.join(os.path.dirname(__file__), "template.mako")) as f:
        print(Template(f.read()).render(
            title=lambda text: f"\033[1m{text}\033[0m",
            indent=lambda text, n: "\n".join(map(lambda line: " " * n + line, text.split("\n"))),
            wordwrap=lambda text, width: "\n".join(textwrap.wrap(text, width)),
            parameter=parameter,
            command=command,
            cli_expressions=cli_expressions,
            env_expressions=env_expressions,
            config_file_expressions=config_file_expressions,
            tree=tree,
            alternatives=alternatives,
            comments=comments
        ).strip("\n"))
        print("")
