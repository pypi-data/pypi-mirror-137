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

import inspect

import six
from six.moves import map, zip


def define_factory_method(method_name, parameter_type):
    """Generate a factory method that creates and appends an instance of the parameter_type.

    The factory method has the signature of the constructor of the parameter type. All mandatory
    parameters in that signature are still mandatory here and all optionals in that signature
    retain their defaults. This way we don't have to specify everything twice. The signature of
    the parameter constructor is unreadable enough and we don't want to introduce new bugs by
    having to maintain the same list twice.

    Example:
    For a parameter_type SwitchParameter of which the __init__ method has the parameters
    (self, name, advanced=True, help="") this method will generate the following method:

      def add_parameter(self, name, advanced=True, help=''):
          self._append_parameter(SwitchParameter(name, advanced=advanced, help=help))
    """
    mandatory_args, optionals, defaults = _get_parameters_of_constructor(parameter_type)
    method_string = (
        "def {method_name}(self, {mandatory_args}, {kwargs}):"
        "    self._append_parameter({parameter_type}({mandatory_args}, {forwarded_args}))"
    ).format(method_name=method_name,
             mandatory_args=", ".join(mandatory_args),
             kwargs=_string_with_assignment_expressions(list(zip(optionals,
                                                                 list(map(_human_readable, defaults))))),
             parameter_type=parameter_type.__name__,
             forwarded_args=_string_with_assignment_expressions(list(zip(optionals, optionals))))
    return compile(method_string, __file__, "exec")


def _human_readable(value):
    """Return a human readable string representation of 'value'."""
    if isinstance(value, type):
        return value.__name__
    else:
        return repr(value)


def _get_parameters_of_constructor(parameter_type):
    """Return a 3-tuple of the required params, optionals and defaults of the optionals."""
    if six.PY2:
        argspec = inspect.getargspec(parameter_type.__init__.__func__)
    else:
        argspec = inspect.getargspec(parameter_type.__init__)
    mandatory_args = argspec.args[1:-len(argspec.defaults)]
    optional_args = argspec.args[-len(argspec.defaults):]
    return (mandatory_args, optional_args, argspec.defaults)


def _string_with_assignment_expressions(vars_to_exprs):
    """Combine a mapping of vars to python literals or names into a single assign expr."""
    return ", ".join(map((lambda var_expr: "%s=%s" % (var_expr[0], var_expr[1])), vars_to_exprs))
