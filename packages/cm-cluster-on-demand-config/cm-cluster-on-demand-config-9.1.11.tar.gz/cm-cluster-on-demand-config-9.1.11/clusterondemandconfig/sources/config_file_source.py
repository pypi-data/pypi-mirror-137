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

import io
import logging
import re

import six.moves.configparser
import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.request

from clusterondemandconfig.exceptions import ConfigLoadError
from clusterondemandconfig.expression_parser import parse_expression
from clusterondemandconfig.global_config import config

from .source import Source

log = logging.getLogger("cluster-on-demand")

COMMENT_UNTIL_END_OF_LINE_REGEX = r"#.*"
URL_IN_CONFIG_FILE_REGEX = r"remote:([^#]+)"


class ConfigFileSource(Source):
    """Parameter value source for the config loader that obtains values from a single ini file."""

    def __init__(self, config_file):
        self.config_file = config_file
        self._parser = None

    def is_enforcing(self):
        return False

    def __str__(self):
        return "file: " + self.config_file  # TODO: show line

    def has_value_for_parameter(self, parameter, configuration):
        for namespace in parameter.namespaces:
            if self.parser.has_option(namespace, parameter.name):
                return True
        return False

    def get_value_for_parameter(self, parameter, configuration):
        assert self.has_value_for_parameter(parameter, configuration)

        try:
            current_value = configuration.get_parameter_value(parameter)
            for namespace in parameter.namespaces:
                if self.parser.has_option(namespace, parameter.name):
                    expression = self.parser.get(namespace, parameter.name)
                    current_value = parse_expression(expression, parameter, current_value)

            return current_value
        except Exception as e:
            raise ConfigLoadError(
                "An error occured when parsing the value for parameter '%s' set in %s:\n\t%s" %
                (parameter.name, self.config_file, e)
            )

    def __eq__(self, other):  # pragma: no cover
        return type(self) == type(other) and self.config_file == other.config_file

    def get_parameters(self):
        for section in self.parser.sections():
            for option in self.parser.options(section):
                yield (section, option)

    @property
    def parser(self) -> six.moves.configparser.ConfigParser:
        if self._parser is None:
            self._parser = _config_parser_for_file(self.config_file)
        return self._parser


def _config_parser_for_file(config_file):
    parser = six.moves.configparser.ConfigParser()
    try:
        log.debug("Using config file: %s" % (config_file))
        if _config_file_contains_remote_link(config_file):
            parser.readfp(_remote_config_file_stream(_url_in_config_file(config_file)))
        else:
            parser.read(config_file)
        return parser
    except six.moves.configparser.Error:
        log.error("Error when parsing config file %s" % (config_file))
        raise ConfigLoadError("Config file %s is not a valid INI file." % (config_file))


def _config_file_contains_remote_link(config_file):
    with open(config_file) as f:
        contents = f.read().strip()
        contents = re.sub(COMMENT_UNTIL_END_OF_LINE_REGEX, "", contents).strip()

        return 1 == len(contents.split("\n")) and contents.startswith("remote:")


def _url_in_config_file(config_file):
    with open(config_file) as f:
        match = re.search(URL_IN_CONFIG_FILE_REGEX, f.read())
        url = match.group(1).strip()
        return url.format(config)


def _remote_config_file_stream(url):
    stream = io.StringIO()
    try:
        log.debug("Downloading remote config file from: %s" % (url))
        stream.write(six.moves.urllib.request.build_opener().open(url).read().decode("utf-8"))
        stream.seek(0)
    except six.moves.urllib.error.URLError:
        log.error("Could not download the configuration from %s, ignoring this source" % (url))
    return stream
