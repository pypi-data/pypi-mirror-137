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

import itertools

from .exceptions import ConfigConstructError


class CommandContext(object):
    """Maintains a related collection of grouped Command instances.

    An instance of this class is passed on to and used by determine_invoked_command to inform the
    user of all known commands and to determine whether the user invocation refers to a valid
    command.
    """

    def __init__(self, cli_expression):
        self.groups = []
        self.name = cli_expression.split(" ")[0]
        self.cli_expression = cli_expression

    def add_group(self, cli_expression, help=None, aliases=None):
        """Create and add a command group to this context."""
        if not cli_expression.startswith(self.cli_expression + " "):
            raise ConfigConstructError("'%s' does not start with '%s'" % (cli_expression, self.cli_expression))

        group_name = cli_expression[len(self.cli_expression):].strip()
        group_aliases = aliases or []

        group = CommandGroup(name=group_name, help=help, aliases=group_aliases, cli_expression=cli_expression)
        self._append_if_no_collision_on_name_or_alias(group, self.groups)

    def add_command(
            self, cli_expression, module, help=None, aliases=None, important_help_sections=None, require_eula=True
    ):
        """Create and add a command to this context."""
        if not cli_expression.startswith(self.cli_expression + " "):
            raise ConfigConstructError("'%s' does not start with '%s'" % (cli_expression, self.cli_expression))
        self._verify_that_module_is_complete(module)

        group = self._group_for_command_with_cli_expression(cli_expression)
        command_name = cli_expression[len(self.cli_expression + " " + group.name):].strip()
        command_aliases = aliases or []
        combined_aliases = [
            "".join(combined_alias)
            for combined_alias in itertools.product(group.aliases, command_aliases)
        ]

        if important_help_sections is None:
            important_help_sections = [module.config_ns]
        important_help_sections = self._normalize_help_section_list(important_help_sections)

        command = Command(
            name=command_name,
            group=group,
            run_command=module.run_command,
            parameters=module.config_ns.parameters,
            help=help,
            aliases=command_aliases,
            combined_aliases=combined_aliases,
            important_help_sections=important_help_sections,
            require_eula=require_eula,
            cli_expression=cli_expression
        )
        self._append_if_no_collision_on_name_or_alias(command, group.commands)

    def command_for_group_and_command_name(self, group_name, command_name):
        for group in self.groups:
            if group.name == group_name or group_name in group.aliases:
                for command in group.commands:
                    if command.name == command_name or command_name in command.aliases:
                        return command
        return None

    def command_for_combined_alias(self, combined_alias):
        for group in self.groups:
            for command in group.commands:
                if combined_alias in command.combined_aliases:
                    return command
        return None

    def _verify_that_module_is_complete(self, module):
        for required in ["run_command", "config_ns"]:
            if not hasattr(module, required):
                raise ConfigConstructError("module '%s' does not have attr %s" % (module.__name__, required))

    def _group_for_command_with_cli_expression(self, cli_expression):
        for group in self.groups:
            if cli_expression.startswith(self.cli_expression + " " + group.name + " "):
                return group
        raise ConfigConstructError("Could not find a group for cli expression '%s'" % cli_expression)

    def _append_if_no_collision_on_name_or_alias(self, new_item, items):
        self._ensure_no_collision_on_name_or_alias(new_item, items)
        items.append(new_item)

    def _ensure_no_collision_on_name_or_alias(self, new_item, existing_items):
        for existing_item in existing_items:
            if existing_item.name == new_item.name:
                raise ConfigConstructError("Cannot add %s '%s' because one with that name already exists." %
                                           (type(new_item).__name__, existing_item.name))

            shared_aliases = list(set(existing_item.aliases).intersection(set(new_item.aliases)))
            if shared_aliases:
                raise ConfigConstructError("Cannot add %s '%s' because one with the aliases %s already exists." %
                                           (type(new_item).__name__, new_item.name, shared_aliases))

    def _normalize_help_section_list(self, help_sections):
        normalized_help_sections = []

        for help_section in help_sections:
            if isinstance(help_section, str):
                normalized_help_sections.append(help_section)
            elif help_section.help_section:
                normalized_help_sections.append(help_section.help_section)

        return normalized_help_sections

    def __iter__(self):
        for group in self.groups:
            yield group

    def commands(self):
        return list(itertools.chain(*map(lambda context: context.commands, self)))

    def parameters(self):
        return list(itertools.chain(*map(lambda context: context.parameters(), self)))


class CommandGroup(object):
    """Represents a group of commands."""

    def __init__(self, name, help, aliases, cli_expression):
        self.commands = []
        self.name = name
        self.help = help
        self.aliases = aliases
        self.cli_expression = cli_expression

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __iter__(self):
        for command in self.commands:
            yield command

    def parameters(self):
        return list(itertools.chain(*map(lambda command: command.parameters, self)))


class Command(object):
    """Represents a single action that a cm-cod-* application can execute."""

    def __init__(
            self, name, group, run_command, parameters, help, aliases, combined_aliases,
            important_help_sections, require_eula, cli_expression
    ):
        self.name = name
        self.group = group
        self.run_command = run_command
        self.parameters = parameters
        self.help = help
        self.aliases = aliases
        self.combined_aliases = combined_aliases
        self.important_help_sections = important_help_sections
        self.require_eula = require_eula
        self.cli_expression = cli_expression

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
