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

import logging

import six

from clusterondemandconfig.parameter import PositionalParameter

from .configuration import Configuration
from .configuration_item import ConfigurationItem
from .configuration_view import ConfigurationView

log = logging.getLogger("cluster-on-demand")


class CommandConfiguration(Configuration, ConfigurationView):
    """Represents the configuration for a single Command. Only stores a single value per parameter."""

    def __init__(self, parameters):
        self._mutable = True
        self._keys_to_items = {parameter.key: ConfigurationItem(parameter) for parameter in parameters}

    def lock(self):
        self._mutable = False

    def view_for_namespace(self, namespace):
        return self

    def set_value(self, parameter, value, source):
        assert not self.is_value_locked_for_parameter(parameter)

        item = self.get_item_for_key(parameter.key)
        item.value, item.source = value, source

    def set_locked_value(self, parameter, value, source):
        assert not self.is_value_locked_for_parameter(parameter)

        item = self.get_item_for_key(parameter.key)
        item.value, item.source, item.locked = value, source, True

    def is_value_locked_for_parameter(self, parameter):
        return self.get_item_for_key(parameter.key).locked

    def get_item_for_key(self, key):
        """Return the ConfigurationItem object that is mapped to the key."""
        if key in self._keys_to_items:
            return self._keys_to_items[key]
        else:
            raise KeyError("Programmer error: The parameter '%s' is not defined within this configuration." % key)

    def get_parameter_value(self, parameter):
        return self.get_item_for_key(parameter.key).value

    def get_source_of_parameter_value(self, parameter):
        return self.get_item_for_key(parameter.key).source

    def reduced_dict(self):
        return self._keys_to_items

    def required_positionals_with_missing_values(self):
        return [config_item.parameter
                for config_item in self._keys_to_items.values()
                if isinstance(config_item.parameter, PositionalParameter)
                and config_item.parameter.require_value
                and config_item.value is None]

    def __getitem__(self, parameter_key):
        """Handle the [] operation. Return the value that was assigned to this parameter."""
        return self.get_item_for_key(parameter_key).value

    def __setitem__(self, parameter_key, value):
        """Handle the []= operation. This is no bueno and could disappear with CM-20154."""
        if not self._mutable:
            log.debug("Dynamic modification of the config object: %s" % (parameter_key))
        self.get_item_for_key(parameter_key).value = value

    def __contains__(self, key):
        return key in self._keys_to_items

    def __iter__(self):
        return six.iteritems(self._keys_to_items)

    def __format__(self, format):
        return str(self[format])
