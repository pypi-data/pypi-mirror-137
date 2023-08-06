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

import glob
import logging
import os

from six.moves import map

from clusterondemand.exceptions import CODException
from clusterondemandconfig import config
from clusterondemandconfig.sources import (
    CLISource,
    ConfigFileSource,
    DynamicDefaultSource,
    EnforcingConfigFileSource,
    ENVSource,
    StaticDefaultSource
)

log = logging.getLogger("cluster-on-demand")


class SourceType:
    """Factory class for Source instances."""
    def __init__(self, parameters, system_config_files, enforcing_config_files):
        self._parameters = parameters
        self._enforcing_config_files = enforcing_config_files
        self._system_config_files = system_config_files

    def static_default(self):
        return [StaticDefaultSource()]

    def enforcing_config_files(self):
        return list(map(
            EnforcingConfigFileSource, _readable_config_files_for_glob_patterns(self._enforcing_config_files)
        ))

    def system_config_files(self):
        if "system_config" in config and config["system_config"]:
            return list(map(ConfigFileSource, _readable_config_files_for_glob_patterns(self._system_config_files)))
        else:
            return []

    def cli_config_files(self):
        if "config" not in config:
            return []

        cli_config_files = []

        for config_file in config["config"] or []:
            if not os.path.isfile(config_file) or not os.access(config_file, os.R_OK):
                raise CODException("Config file %s does not exist or is not readable" % (config_file))
            cli_config_files.append(config_file)

        return list(map(ConfigFileSource, cli_config_files))

    def env(self):
        return [ENVSource()]

    def loose_cli(self):
        # TODO: improve name, a loose cli source simply doesn't complain about unknown flags.
        return [CLISource(self._parameters, strict=False)]

    def strict_cli(self):
        return [CLISource(self._parameters, strict=True)]

    def dynamic_default(self):
        return [DynamicDefaultSource()]


def generate_sources(source_order, parameters, system_config_files, enforcing_config_files):
    """Convert `source_order` into an ordered list of Source instances.

    `source_order` is expected to be a list of unbound methods of SourceType. These methods take an
    instance of SourceType and return a list of Source instances.
    """
    sources = []
    factory = SourceType(parameters, system_config_files, enforcing_config_files)

    for source in source_order:
        sources.extend(source(factory))

    return sources


def _readable_config_files_for_glob_patterns(config_file_globs):
    config_file_paths = []

    for config_file_glob in config_file_globs:
        log.debug("Searching for config files at: %s" % (config_file_glob))
        for config_file_path in sorted(glob.glob(config_file_glob)):
            if not os.access(config_file_path, os.R_OK):
                raise CODException("Config file %s is not readable" % (config_file_path))
            config_file_paths.append(config_file_path)

    return config_file_paths
