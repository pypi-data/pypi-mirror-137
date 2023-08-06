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

import tempfile

import six

from clusterondemand.command_runner import sys_argv
from clusterondemand.testutils import environ
from clusterondemandconfig import ConfigNamespace
from clusterondemandconfig.parameter import SimpleParameter


class with_text_in_config_file(object):
    def __init__(self, text):
        self.text = text

    def __call__(self, func):
        def wrapper(_self, config_files=None, **kwargs):
            config_files = config_files or []

            with tempfile.NamedTemporaryFile(mode="w+") as tmpfile:
                tmpfile.write(self.text)
                tmpfile.flush()
                config_files.append(tmpfile.name)

                return func(_self, config_files=config_files, **kwargs)
        return wrapper


class with_config_file(object):
    def __init__(self, contents):
        self.contents = contents

    def __call__(self, func):
        def wrapper(_self, config_files=None, **kwargs):
            config_files = config_files or []

            with tempfile.NamedTemporaryFile(mode="w+") as tmpfile:
                tmpfile.write(self.contents)
                tmpfile.flush()
                config_files.append(tmpfile.name)

                return func(_self, config_files=config_files, **kwargs)
        return wrapper


class with_values_in_config_file(object):
    def __init__(self, names_to_values):
        self.names_to_values = names_to_values

    def __call__(self, func):
        def wrapper(_self, parameters=None, config_files=None, **kwargs):
            parameters = parameters or []
            config_files = config_files or []
            _ensure_parameters_in_list(self.names_to_values, parameters)

            fragments = ["%s = %s" % (name, value) for (name, value) in six.iteritems(self.names_to_values)]
            with tempfile.NamedTemporaryFile(mode="w+") as tmpfile:
                tmpfile.write("[some-namespace]\n" + "\n".join(fragments))
                tmpfile.flush()
                config_files.append(tmpfile.name)

                return func(_self, parameters=parameters, config_files=config_files, **kwargs)
        return wrapper


class with_values_in_os_environ(object):
    def __init__(self, names_to_values):
        self.names_to_values = names_to_values

    def __call__(self, func):
        def wrapper(_self, parameters=None, **kwargs):
            parameters = parameters or []
            _ensure_parameters_in_list(self.names_to_values, parameters)

            environs = {"COD_" + name.upper(): value for (name, value) in six.iteritems(self.names_to_values)}
            with environ(environs):
                return func(_self, parameters=parameters, **kwargs)
        return wrapper


class with_values_in_sys_argv(object):
    def __init__(self, names_to_values):
        self.names_to_values = names_to_values

    def __call__(self, func):
        def wrapper(_self, parameters=None, **kwargs):
            parameters = parameters or []
            _ensure_parameters_in_list(self.names_to_values, parameters)

            fragments = ["--%s %s" % (name, value) for (name, value) in six.iteritems(self.names_to_values)]
            with sys_argv("cm-cod-os " + " ".join(fragments)):
                return func(_self, parameters=parameters, **kwargs)
        return wrapper


class with_sys_argv(object):
    def __init__(self, args):
        self.args = args

    def __call__(self, func):
        def wrapper(_self, **kwargs):
            with sys_argv(self.args):
                return func(_self, **kwargs)
        return wrapper


def _ensure_parameters_in_list(names_to_values, parameter_list):
    for (name, value) in six.iteritems(names_to_values):
        if not [parameter for parameter in parameter_list if parameter.name == name]:
            parameter = SimpleParameter(name)
            parameter.namespace = ConfigNamespace("some-namespace")
            parameter.namespaces.append("some-namespace")
            parameter_list.append(parameter)
