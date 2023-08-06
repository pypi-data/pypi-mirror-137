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

import clusterondemandconfig

from .configuration_view import ConfigurationView


class GlobalConfiguration(ConfigurationView):
    """The configuration that is globally available. Only meant to wrap an actual CommandConfiguration object."""

    config = {}

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        # TODO: CM-20154, mutability is doubleplusungood.
        self.config[key] = value

    def __contains__(self, key):
        return key in self.config

    def get_item_for_key(self, key):
        return self.config.get_item_for_key(key)

    def is_item_set_explicitly(self, key):
        return isinstance(self.get_item_for_key(key).source, clusterondemandconfig.sources.CLISource)

    def __format__(self, fmt):
        return str(self[fmt])
