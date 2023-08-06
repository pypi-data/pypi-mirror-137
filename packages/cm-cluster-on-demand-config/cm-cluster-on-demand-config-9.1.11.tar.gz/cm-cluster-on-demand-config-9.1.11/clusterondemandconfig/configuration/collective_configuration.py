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

from .configuration import Configuration
from .configuration_for_namespace_view import ConfigurationForNamespaceView
from .configuration_item import ConfigurationItem

log = logging.getLogger("cluster-on-demand")


class CollectiveConfiguration(Configuration):
    """Contains the parameter to value mapping for multiple commands. Can store multiple values for a single parameter.

    Takes namespaces into account. A parameter can have multiple namespaces and setting a value for
    a more specific one does not change the value of the more generic one. For every parameter and
    for every namespace in which parameter appears, a ConfigurationItem instance stores the value of
    that parameter in that namespace.

    When a value is set for a parameter in a certain namespace, then that change is cascaded down to
    configuration items for that same parameter in descending namespaces.
    """

    def __init__(self, parameters):
        self._unique_names_to_items = _construct_unique_names_to_items_dictionary(parameters)
        self._item_hierarchy = _construct_item_hierarchy(parameters, self._unique_names_to_items)

    def view_for_namespace(self, namespace):
        return ConfigurationForNamespaceView(self, namespace)

    def set_value(self, parameter, value, source):
        for item in self._all_items_for_parameter(parameter):
            if not item.locked:
                item.value, item.source = value, source

    def set_locked_value(self, parameter, value, source):
        for item in self._all_items_for_parameter(parameter):
            if not item.locked or item.source == source:
                item.value, item.source, item.locked = value, source, True

    def is_value_locked_for_parameter(self, parameter):
        return self._item_for_parameter(parameter).locked

    def has_item_for_unique_key(self, unique_key):
        return unique_key in self._unique_names_to_items

    def get_item_for_unique_key(self, unique_key):
        if unique_key not in self._unique_names_to_items:
            raise KeyError("The configuration item with the key %s is not known" % unique_key)
        return self._unique_names_to_items[unique_key]

    def get_parameter_value(self, parameter):
        return self._item_for_parameter(parameter).value

    def get_source_of_parameter_value(self, parameter):
        return self._item_for_parameter(parameter).source

    def reduced_dict(self):
        """Generate dictionary with all parameters in all their namespaces, but only when they have an actual value.

        A namespace, parameter pair is only mentioned when it is either the original one, or when
        the value of the parameter for that namespace differs from the value of that parameter in the parent namespace.
        """
        return {
            unique_name: item
            for (unique_name, item) in six.iteritems(self._unique_names_to_items)
            if item.parameter.parent is None
            or item.value != self._unique_names_to_items[_unique_name(item.parameter.parent)].value
        }

    def __iter__(self):
        return six.iteritems(self._unique_names_to_items)

    def to_dict(self):
        """Generate dictionary with all parameters in all their namespaces."""
        return {key: item.value for (key, item) in self}

    def _all_items_for_parameter(self, parameter):
        queue = [self._item_for_parameter(parameter)]
        while queue:
            item = queue.pop(0)
            yield item
            if _unique_name(item.parameter) in self._item_hierarchy:
                queue.extend(self._item_hierarchy[_unique_name(item.parameter)])

    def _item_for_parameter(self, parameter):
        return self._unique_names_to_items[_unique_name(parameter)]


def _construct_unique_names_to_items_dictionary(parameters):
    return {
        _unique_name(parameter): ConfigurationItem(parameter)
        for parameter in parameters
    }


def _construct_item_hierarchy(parameters, item_dictionary):
    hierarchy = {}

    for parameter in parameters:
        if parameter.parent is None:
            continue

        parent_name = _unique_name(parameter.parent)
        parameter_name = _unique_name(parameter)
        if parent_name not in hierarchy:
            hierarchy[parent_name] = []
        hierarchy[parent_name].append(item_dictionary[parameter_name])

    return hierarchy


def _unique_name(parameter):
    return parameter.namespaces[-1] + "." + parameter.name
