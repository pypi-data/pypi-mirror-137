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

from clusterondemandconfig.exceptions import ConfigValueIsLockedError
from clusterondemandconfig.parameter import PositionalParameter
from clusterondemandconfig.sources import CLISource, ENVSource, StaticDefaultSource

log = logging.getLogger("cluster-on-demand")


def can_obtain_parameter_value_from_source(parameter, source):
    """Some values may not be obtained from the env or configuration file."""
    if isinstance(parameter, PositionalParameter):
        return isinstance(source, CLISource) or isinstance(source, StaticDefaultSource)
    else:
        return True


def raise_or_warn_about_locked_value(configuration, parameter, source):
    if isinstance(source, CLISource):
        raise ConfigValueIsLockedError(
            "Can not set value for parameter '%s'; the value set in %s cannot be overridden." %
            (parameter.name, configuration.get_source_of_parameter_value(parameter))
        )
    elif isinstance(source, ENVSource):
        warn_about_locked_value(configuration, parameter, source)


def warn_about_locked_value(configuration, parameter, source):
    log.warn("The value of %s is ignored because another value is enforced in %s." %
             (parameter.env, configuration.get_source_of_parameter_value(parameter)))


def assign_value(configuration, parameter, source):
    value = source.get_value_for_parameter(parameter, configuration)

    if source.is_enforcing():
        configuration.set_locked_value(parameter, value, source)
    else:
        configuration.set_value(parameter, value, source)
