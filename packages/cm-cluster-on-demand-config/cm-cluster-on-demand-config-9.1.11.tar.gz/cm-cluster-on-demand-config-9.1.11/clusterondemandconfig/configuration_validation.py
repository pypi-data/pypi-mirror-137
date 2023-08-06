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

import getpass
import logging
import re
from os import R_OK, access
from os.path import exists, expanduser, expandvars, isdir, isfile, realpath

from .exceptions import ConfigLoadError

log = logging.getLogger("cluster-on-demand")


def validate_configuration(configuration):
    parameters = [config_item.parameter for _, config_item in configuration]

    for namespace in set([parameter.namespace for parameter in parameters]):
        for validation in namespace.validation:
            validation(namespace, configuration)

    for parameter in parameters:
        if not parameter.validation:
            continue
        validations = parameter.validation if isinstance(parameter.validation, list) else [parameter.validation]
        for validation in validations:
            validation(parameter, configuration)


def cannot_use_together(*parameter_names):
    """Prevents multiple of the named parameters to have a non-None value."""
    def validate(namespace, configuration):
        configured_items = [
            item
            for item in [configuration.get_item_for_key(name) for name in parameter_names]
            if item.value is not None
        ]

        if 1 < len(configured_items):
            raise ConfigLoadError(
                "Cannot set both %s simultaneously" %
                ", ".join(["%s=%s" % (item.parameter.name, item.value) for item in configured_items])
            )

    return validate


def cannot_enable_together(*parameter_names):
    """Prevents multiple of the boolean parameters to be enabled at the same time."""
    def validate(namespace, configuration):
        configured_items = [
            item
            for item in [configuration.get_item_for_key(name) for name in parameter_names]
            if item.value
        ]

        if 1 < len(configured_items):
            raise ConfigLoadError(
                "Cannot enable both %s simultaneously" %
                ", ".join(["%s=%s" % (item.parameter.name, item.value) for item in configured_items])
            )

    return validate


def requires_other_parameters_to_be_set(required_parameter_names):
    """
    Ensure that if the validated parameter is set, the other, required, parameters is also set.
    """
    def validate(parameter, configuration):
        item = configuration.get_item_for_key(parameter.name)
        if item.value:
            required_items = [configuration.get_item_for_key(name) for name in required_parameter_names]
            parameters_not_set = [item.parameter.name for item in required_items if not item.value]
            if parameters_not_set:
                raise ConfigLoadError(
                    "Using '%s' requires '%s' to also be set" % (item.parameter.name, ", ".join(parameters_not_set)))

    return validate


def if_disabled_require_other_paramaters_to_be_disabled(required_parameter_names):
    def validate(parameter, configuration):
        item = configuration.get_item_for_key(parameter.name)
        if not item.value:
            required_items = [configuration.get_item_for_key(name) for name in required_parameter_names]
            parameters_set = [item.parameter.name for item in required_items if item.value]
            if parameters_set:
                raise ConfigLoadError(
                    "Disabling '%s' requires '%s' to also be disabled/false."
                    % (item.parameter.name, ", ".join(parameters_set)))

    return validate


def requires_other_parameter_to_be_set(required_parameter_name):
    return requires_other_parameters_to_be_set([required_parameter_name])


def require_exactly_one_to_be_set(*parameter_names):
    """Require EXACTLY one parameter to be set (no more, no fewer)"""
    def validate(namespace, configuration):
        configured_items = [
            item
            for item in [configuration.get_item_for_key(name) for name in parameter_names]
            if item.value is not None
        ]

        if 1 != len(configured_items):
            raise ConfigLoadError(
                "Exactly only one parameter from these is allowed and required %s. "
                "More or less than one are not allowed. "
                "Number of parameters configured: %s" % (", ".join(parameter_names), len(configured_items)))

    return validate


def ask_for_password_if_not_set(password_name, custom_prompt, custom_error, username_name=None):
    """ If parameter is not set, displays the custom prompt, followed by
    a password input prompt (i.e. prompt which does not display typed-in characters)

    If "username_name" is set, function will attempt to use the config property of that name
    to replace any "{username}" within the prompt (if present).
    """

    def _ask_for_password(configuration):
        prompt = custom_prompt
        if username_name:
            username_item = configuration.get_item_for_key(username_name)
            prompt = custom_prompt.format(username=username_item.value)

        log.info(prompt)

        # Empty prompt, because otherwise it might cause issue as
        # in the COD container we might not have a tty
        return getpass.getpass("")

    def wrapper(parameter, configuration):
        password_item = configuration.get_item_for_key(password_name)

        if not password_item.value:
            password = _ask_for_password(configuration)

            if not password:
                raise ConfigLoadError(custom_error)

            password_item.value = password

    return wrapper


def may_not_equal_none(parameter, configuration):
    if configuration[parameter.key] is None:
        raise ConfigLoadError(
            "parameter '%s' may not be empty. Either set it on the cli with '%s', as an env var"
            " through '%s=' or set it in a config file." % (parameter.key, parameter.default_flag, parameter.env))


def must_be_nonnegative(parameter, configuration):
    if configuration[parameter.key] < 0:
        raise ConfigLoadError(
            f"parameter '{parameter.name}' must be zero or a positive number. Either set it on the cli with "
            f"{parameter.default_flag}, as an env var through {parameter.env} or set it in a config file."
        )


def must_be_multiple_of(value):
    """Check if the parameter is the multiple of a given integer"""
    def validate(parameter, configuration):
        item = configuration.get_item_for_key(parameter.name)
        if (item.value % value):
            raise ConfigLoadError(
                f"parameter '{parameter.name}' must be a multiple of {value}. Either set it on the cli with "
                f"{parameter.default_flag}, as an env var through {parameter.env} or set it in a config file."
            )

    return validate


def require_at_least_one_to_be_set(*parameter_names):
    """exactly one, out of several, needs to be set."""
    def validate(namespace, configuration):
        configured_items = [
            item
            for item in [configuration.get_item_for_key(name) for name in parameter_names]
            if item.value is not None
        ]

        if 0 == len(configured_items):
            raise ConfigLoadError(
                "One, or more, of these parameters must be set: " + ", ".join([name for name in parameter_names])
            )

    return validate


def other_parameter_must_not_equal(parameter_name, value):
    """
    Ensure that if the validated parameter is set, the other parameter is not set to the defined value
    """
    def validate(parameter, configuration):
        item = configuration.get_item_for_key(parameter.name)
        other_item = configuration.get_item_for_key(parameter_name)

        if item.value and other_item.value == value:
            raise ConfigLoadError(
                "Using '%s' requires '%s' to not be set to '%s'" % (
                    item.parameter.name,
                    other_item.parameter.name,
                    value
                ))

    return validate


def if_set_file_exists_and_readable(parameter, configuration):
    item = configuration.get_item_for_key(parameter.name)
    if item.value:
        file_path = expandvars(expanduser(item.value))
        if not exists(file_path):
            raise ConfigLoadError(f"Specified file '{file_path}' does not exist")
        file_path = realpath(file_path)
        if isdir(file_path):
            raise ConfigLoadError(f"Specified file '{file_path}' is a directory")
        if not isfile(file_path):
            raise ConfigLoadError(f"Specified file '{file_path}' is not a file")
        if not access(file_path, R_OK):
            raise ConfigLoadError(f"Specified file '{file_path}' cannot be read, permission denied")


def match_http_proxy_format(parameter, configuration):
    username_password = r"(?:(\w+)(?::(\w+))?@)?"
    ipv4_address = r"((?:\d{1,3})(?:\.\d{1,3}){3})"
    ipv6_seg = r"(?:(?:[0-9a-fA-F]){1,4})"
    ipv6_groups = (
        r"(?:" + ipv6_seg + r":){7,7}" + ipv6_seg,
        r"(?:" + ipv6_seg + r":){1,7}:",
        r"(?:" + ipv6_seg + r":){1,6}:" + ipv6_seg,
        r"(?:" + ipv6_seg + r":){1,5}(?::" + ipv6_seg + r"){1,2}",
        r"(?:" + ipv6_seg + r":){1,4}(?::" + ipv6_seg + r"){1,3}",
        r"(?:" + ipv6_seg + r":){1,3}(?::" + ipv6_seg + r"){1,4}",
        r"(?:" + ipv6_seg + r":){1,2}(?::" + ipv6_seg + r"){1,5}",
        ipv6_seg + r":(?:(?::" + ipv6_seg + r"){1,6})",
        r":(?:(?::" + ipv6_seg + r"){1,7}|:)",
        r"fe80:(?::" + ipv6_seg + r"){0,4}%[0-9a-zA-Z]{1,}",
    )
    ipv6_address = "|".join(["(?:{})".format(g) for g in ipv6_groups[::-1]])
    hostname = r"(([a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])"
    port = r"(:(\d{1,5}))?"
    http_proxy_format_regex = (r"^(http://)%s(%s|%s|%s)%s$" % (username_password, ipv4_address, hostname,
                               ipv6_address, port))
    compiled_http_proxy_format_regex = re.compile(http_proxy_format_regex)
    param_value = configuration[parameter.key]
    if param_value and not compiled_http_proxy_format_regex.match(param_value):
        raise ConfigLoadError(
            f"The provided http proxy: '{param_value}' does not match the expected formats: "
            "'http://[user:password@]host[.domain]:port_number' or "
            "'http://[user:password@]IP_ADDRESS:port_number'"
        )


def ignore_if_default(other_validation):
    """
    Don't run validation if the validated parameter has default value
    """
    def validate(parameter, configuration):
        item = configuration.get_item_for_key(parameter.name)
        if item.value != item.parameter.default:
            validations = other_validation if isinstance(other_validation, list) else [other_validation]
            for validation in validations:
                validation(parameter, configuration)

    return validate
