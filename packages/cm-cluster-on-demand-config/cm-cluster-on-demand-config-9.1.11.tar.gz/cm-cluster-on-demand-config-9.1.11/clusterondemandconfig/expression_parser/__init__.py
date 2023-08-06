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

from .evaluator import evaluate
from .grammar import Grammar, Token
from .parser import parse
from .tokenizer import tokenize


def parse_expression(expression, parameter, current_value):
    if "None" == expression:
        return None
    elif isinstance(parameter.type, list):
        if not expression:
            return []
        return _parse_enum_expression(parameter, expression, current_value)
    elif not expression:
        return None
    else:
        return parse_single_value(parameter, remove_any_wrapping_symbols(expression))


def _parse_enum_expression(parameter, expression, current_value):
    tokens = [Token.identifier_for_string(parameter.key)] + Grammar.TOKENS
    mapping = {parameter.key: current_value or []}

    return evaluate(parse(tokenize(expression, tokens)), parameter, mapping)
