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

from .configuration_view import ConfigurationView


class ConfigurationForNamespaceView(ConfigurationView):
    def __init__(self, configuration, namespace):
        self.configuration = configuration
        self.namespace = namespace

    def __getitem__(self, key):
        return self.get_item_for_key(key).value

    def __contains__(self, key):
        return self.has_item_for_key(key) and self.get_item_for_key(key) is not None

    def has_item_for_key(self, key):
        return self.configuration.has_item_for_unique_key("%s.%s" % (self.namespace.name, key))

    def get_item_for_key(self, key):
        return self.configuration.get_item_for_unique_key("%s.%s" % (self.namespace.name, key))

    def __format__(self, format):
        return str(self[format])
