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

from ..parser_utils import boolean_parser
from .optional_parameter import OptionalParameter
from .parameter_creation_completion import complete_env, complete_flags, complete_help_text, complete_key
from .parameter_creation_validation import (
    FN_TYPE,
    ensure_default_method_has_correct_signature,
    ensure_env_is_valid,
    ensure_flags_are_valid,
    ensure_key_is_valid,
    ensure_name_is_valid,
    ensure_validations_are_valid,
    one_of,
    validate_attr_types
)


class SwitchParameter(OptionalParameter):
    def __init__(self, name, advanced=False, boot=False, default=False, env=None, flags=None, help="",
                 help_section=None, key=None, validation=None):
        super(SwitchParameter, self).__init__(
            name, advanced=advanced, boot=boot, default=default, env=env, flags=flags, help=help,
            help_section=help_section, help_varname=None, key=key, parser=boolean_parser, secret=False, serializer=str,
            type=bool, validation=validation
        )
        self.validate_attributes()
        self.complete_unspecified_attributes()
        self.validate_attributes()

    def validate_attributes(self):
        validate_attr_types(self, {
            "advanced": bool,
            "boot": bool,
            "name": str,
            "default": one_of(bool, FN_TYPE),
            "env": one_of(str, None),
            "flags": one_of([str], None),
            "help": str,
            "help_section": one_of(str, None),
            "help_varname": one_of(str, None),
            "key": one_of(str, None),
            "validation": one_of(FN_TYPE, [FN_TYPE], None),
        })

        ensure_name_is_valid(self)
        if callable(self.default):
            ensure_default_method_has_correct_signature(self)
        ensure_env_is_valid(self)
        ensure_flags_are_valid(self)
        ensure_key_is_valid(self)
        ensure_validations_are_valid(self)

    def complete_unspecified_attributes(self):
        complete_env(self)
        complete_flags(self)
        complete_help_text(self)
        complete_key(self)
