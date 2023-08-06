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

from clusterondemandconfig.configuration import CommandConfiguration

from .generate_sources import SourceType, generate_sources


def load_boot_configuration_for_command(command):
    parameters = [parameter for parameter in command.parameters if hasattr(parameter, "boot") and parameter.boot]

    order_of_sources = [
        SourceType.static_default,
        SourceType.env,
        SourceType.loose_cli,
        SourceType.dynamic_default
    ]
    sources = generate_sources(order_of_sources, parameters, [], [])

    configuration = CommandConfiguration(parameters)
    _load_configuration_from_sources(configuration, sources, parameters)
    return configuration


def _load_configuration_from_sources(configuration, sources, parameters):
    for source in sources:
        for parameter in parameters:
            if source.has_value_for_parameter(parameter, configuration):
                value = source.get_value_for_parameter(parameter, configuration)

                configuration.set_value(parameter, value, source)
