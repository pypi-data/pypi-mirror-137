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

from clusterondemandconfig.config_file_encoding import remove_any_wrapping_symbols
from clusterondemandconfig.parser_utils import parse_single_value


def evaluate(parse_tree, parameter, mapping):
    """Take a parse tree and convert it to a single value or a list of values."""
    node_type, child_or_children = parse_tree

    if "expression" == node_type:
        result = evaluate(child_or_children[0], parameter, mapping)
        if 3 == len(child_or_children):
            result += evaluate(child_or_children[2], parameter, mapping)
        return result
    elif "item" == node_type:
        return evaluate(child_or_children[0], parameter, mapping)
    elif "enumeration" == node_type:
        result = [evaluate(child_or_children[0], parameter, mapping)]
        if 3 == len(child_or_children):
            result += evaluate(child_or_children[2], parameter, mapping)
        return result
    elif "LITERAL" == node_type:
        return parse_single_value(parameter, remove_any_wrapping_symbols(child_or_children.text))
    elif "IDENTIFIER" == node_type:
        assert child_or_children.text in mapping
        return mapping[child_or_children.text]
    else:
        assert False, "Invalid node_type %s" % (node_type)
