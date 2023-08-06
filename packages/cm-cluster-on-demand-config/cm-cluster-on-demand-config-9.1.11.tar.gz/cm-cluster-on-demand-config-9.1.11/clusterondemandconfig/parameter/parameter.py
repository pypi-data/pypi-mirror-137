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


class Parameter(object):
    """A struct class that acts as an abstract supertype for all configuration parameters."""

    def __init__(self, name, default, help, help_section, help_varname, key, parser,
                 secret, serializer, type, validation):
        self.name = name
        self.default = default
        self.help = help
        self.help_section = help_section
        self.help_varname = help_varname
        self.key = key
        self.parser = parser
        self.secret = secret
        self.serializer = serializer
        self.type = type
        self.validation = validation
        # TODO: fix following two parameters, should they be merged or should names be different?
        self.namespace = None  # type: ConfigNamespace # noqa: F821
        self.namespaces = []  # type: [str]
        self.parent = None  # type: Parameter

    def __hash__(self):  # pragma: no cover
        return hash(str(self))

    def __repr__(self):  # pragma: no cover
        return "<%s: %s>" % (self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):  # pragma: no cover
        return not self == other

    def __copy__(self):
        copy = type(self).__new__(self.__class__)
        copy.__dict__.update(self.__dict__)
        copy.parent = self
        return copy

    @property
    def ancestor(self):
        return self if self.parent is None else self.parent.ancestor
