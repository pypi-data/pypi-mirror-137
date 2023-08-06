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

from .parameter import Parameter


class OptionalParameter(Parameter):
    def __init__(self, name, advanced, boot, default, env, flags, help, help_section, help_varname,
                 key, parser, secret, serializer, type, validation):
        super(OptionalParameter, self).__init__(
            name, default, help, help_section, help_varname, key, parser, secret, serializer,
            type, validation
        )
        self.advanced = advanced
        self.boot = boot
        self.env = env
        self.flags = flags or []

    @property
    def default_flag(self):
        return "--" + self.name.replace("_", "-")

    @property
    def all_flags(self):
        return [self.default_flag] + self.flags

    def flag_with_prefix(self, prefix):
        return "--" + prefix + "-" + self.name.replace("_", "-")
