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

import six
from six.moves import map

from ..exceptions import ConfigConstructError

FN_TYPE = type(lambda: None)
VALID_ENV_REGEX = r"\A[A-Z_][A-Z0-9_]*\Z"  # IEEE Std 1003.1-2001, section 8.1
VALID_KEY_REGEX = r"\A[a-zA-Z_][a-zA-Z0-9_]*\Z"  # Python Language Reference, section 2.3
VALID_FLAG_REGEX = r"\A(-|--)[a-zA-Z0-9][a-zA-Z0-9-_]*\Z"
VALID_NAME_REGEX = r"\A[a-z][a-z0-9_]+\Z"  # To allow easy generation of valid key, env and flag


def one_of(*types):
    return list(types)


def ensure_name_is_valid(parameter):
    if not re.match(VALID_NAME_REGEX, parameter.name):
        raise _bad_value_error(parameter, "name", "must match regex %s" % VALID_NAME_REGEX)


def ensure_default_is_a_choice(parameter):
    if not parameter.choices or parameter.default is None:
        return
    elif parameter.default not in parameter.choices:
        raise _bad_value_error(parameter, "default", "is not a member of {name}.choices {choices}")


def ensure_default_is_a_subset_of_choices(parameter):
    if not parameter.choices or parameter.default is None:
        return
    elif any(set(parameter.default) - set(parameter.choices)):
        raise _bad_value_error(parameter, "default", "is not a subset of {name}.choices {choices}")


def ensure_default_and_type_are_compatible(parameter):
    if parameter.default is None or ([] == parameter.default and isinstance(parameter.type, list)):
        return
    elif callable(parameter.default):
        return
    elif parameter.type and type_of_value(parameter.default) != parameter.type:
        raise _bad_value_error(parameter, "default", "is not of type {type}".format(
            type=_human_readable_type_name(parameter.type)
        ))


def ensure_default_method_has_correct_signature(parameter):
    if callable(parameter.default) and 2 != parameter.default.__code__.co_argcount:
        raise _bad_value_error(parameter, "default", "must have arity of 2")


def ensure_key_is_valid(parameter):
    if parameter.key and not re.match(VALID_KEY_REGEX, parameter.key):
        raise _bad_value_error(parameter, "key", "does not match regex %s" % VALID_KEY_REGEX)


def ensure_env_is_valid(parameter):
    if parameter.env and not re.match(VALID_ENV_REGEX, parameter.env):
        raise _bad_value_error(parameter, "env", "does not match regex %s" % VALID_ENV_REGEX)


def ensure_flags_are_valid(parameter):
    if not parameter.flags:
        return
    for flag in parameter.flags:
        if not re.match(VALID_FLAG_REGEX, flag):
            raise ConfigConstructError("%s flag %s does not match regex %s" % (parameter.name, flag, VALID_FLAG_REGEX))


def ensure_parser_and_serializer_are_valid(parameter):
    if isinstance(parameter.parser, FN_TYPE) and 1 != parameter.parser.__code__.co_argcount:
        raise _bad_value_error(parameter, "parser", "must have arity of 1")
    if isinstance(parameter.serializer, FN_TYPE) and 1 != parameter.serializer.__code__.co_argcount:
        raise _bad_value_error(parameter, "serializer", "must have arity of 1")


def ensure_validations_are_valid(parameter):
    validations = parameter.validation
    if validations:
        for validation in (validations if isinstance(validations, list) else [validations]):
            if 2 != validation.__code__.co_argcount:
                raise _bad_value_error(parameter, "validation", "must have arity of 2")


def ensure_choices_are_valid(parameter):
    if parameter.choices is None:
        return
    elif 0 == len(parameter.choices):
        raise _bad_value_error(parameter, "choices", "must either be None or a non-empty list")
    elif 1 < len(set(map(type, parameter.choices))):
        raise _bad_value_error(parameter, "choices", "must all be of the same type")


def ensure_choices_are_compatible_with_type(parameter):
    if not parameter.choices or parameter.type is None:
        return
    if isinstance(parameter.type, list):
        if parameter.type != type_of_value(parameter.choices):
            raise _bad_value_error(parameter, "choices", "does not match type {type}")
    elif [parameter.type] != type_of_value(parameter.choices):
        raise _bad_value_error(parameter, "choices", "does not match type [{type}]")


def ensure_choices_are_compatible_with_help_choices(parameter):
    if parameter.help_choices and any(set(parameter.help_choices.keys()) - set(parameter.choices)):
        raise _bad_value_error(parameter, "help_choices", "has keys not in {name}.choices {choices}")


def type_of_value(value):
    """Return type of value, taking list types into account."""
    if isinstance(value, list):
        return _unique(list(map(type_of_value, value)))
    else:
        return type(value)


def validate_attr_types(parameter, attrs_to_types):
    """Check the python types of the attributes of 'parameter'."""
    for (attr, types) in six.iteritems(dict(attrs_to_types)):
        value = getattr(parameter, attr)

        if not isinstance(types, list):
            types = [types]

        if not any(_value_is_of_type(value, t) for t in types):
            raise ConfigConstructError(
                "{name}.{attr} has invalid type {type}, should {be_one_of} {types}".format(
                    name=parameter.name, attr=attr,
                    type=_human_readable_type_name(type_of_value(value)),
                    be_one_of="be" if 1 == len(types) else "be one of",
                    types=", ".join(map(_human_readable_type_name, types))
                )
            )


def _value_is_of_type(value, t):
    """Return true if value is of the type represented by t. t can be a type, a list or None."""
    if isinstance(t, type):
        return isinstance(value, t)
    elif t is None:
        return value is None
    elif isinstance(t, list):
        return isinstance(value, list) and all(_value_is_of_type(v, t[0]) for v in value)
    assert False, "t is either type, None or list, but was: %s" % (type(t))


def _human_readable_type_name(t):
    """Return a human readable string representation of the type."""
    if isinstance(t, type):
        return t.__name__
    elif t is None:
        return "None"
    elif isinstance(t, list):
        return "list([%s])" % (", ".join(sorted(map(_human_readable_type_name, t))))
    assert False, "t is either type, None or list, but was: %s" % (type(t))


def _bad_value_error(parameter, attr, msg):
    """Generate a ConfigConstructError with msg, which can contain format references to attributes."""
    mapping = {"attr": attr, "value": repr(getattr(parameter, attr))}
    mapping.update(parameter.__dict__)
    return ConfigConstructError(("{name}.{attr} (= {value}) %s" % msg).format(**mapping))


def _unique(lst):
    """An alternative to set() that *can* deal with lists."""
    unique_values = []
    for value in lst:
        if value not in unique_values:
            unique_values.append(value)
    return unique_values
