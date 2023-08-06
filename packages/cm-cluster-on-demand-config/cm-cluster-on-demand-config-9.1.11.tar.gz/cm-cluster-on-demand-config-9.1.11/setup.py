#!/usr/bin/env python
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

import sys
from pathlib import Path

from setuptools import find_packages, setup

try:
    # Import version file directly to avoid __init__.py execution.
    # Otherwise it causes importing deps which are not installed yet.
    sys.path.append(str(Path(__file__).absolute().parent / "clusterondemandconfig"))
    from _version import version as __version__
except ImportError:
    from setuptools_scm import get_version
    __version__ = get_version(
        root="..",
        relative_to="__file__",
        write_to="cluster-on-demand-config/clusterondemandconfig/_version.py"
    )

with open("README.md", "r") as file_in:
    readme = file_in.read()

setup(
    name="cm-cluster-on-demand-config",
    version=__version__,
    description="Bright Computing COD configuration library",
    author="Cloudteam",
    author_email="cloudteam@brightcomputing.com",
    url="https://www.brightcomputing.com/",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_data={"clusterondemandconfig": [
        "explain/template.mako",
        "tab_completion/template.sh.mako",
    ]},
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.7",
    tests_require=["pytest", "pycoverage"],
    install_requires=[
        "mako>=0.8.1",
        "prettytable~=0.7.2",
    ],
    setup_requires=["setuptools_scm>=4.1.2"]
)
