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

import textwrap

from ..config_file_encoding import encode

MAX_DESCRIPTION_WIDTH = 80


def generate_description(item):
    help_fragments = []

    if item.parameter.help:
        help_fragments.extend(_text_wrap(item.parameter.help))
    if item.parameter.default is not None and item.parameter.default != item.value:
        help_fragments.append("# default=%s" % (encode(item.parameter, item.parameter.default)))

    return "\n".join(help_fragments)


def _text_wrap(text):
    return ["# " + line for line in textwrap.wrap(text, MAX_DESCRIPTION_WIDTH - len("# "))]
