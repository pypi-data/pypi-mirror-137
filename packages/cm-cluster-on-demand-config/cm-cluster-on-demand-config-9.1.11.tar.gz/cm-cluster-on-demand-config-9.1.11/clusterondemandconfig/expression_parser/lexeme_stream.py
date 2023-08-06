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


class LexemeStream():
    """A stateful wrapper around a list of lexemes."""
    def __init__(self, lexemes):
        self._index = 0
        self._lexemes = lexemes

    def __next__(self):
        if self._index < len(self._lexemes):
            lexeme = self._lexemes[self._index]
            self._index += 1
            return lexeme
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def peek(self):
        if self._index < len(self._lexemes):
            return self._lexemes[self._index]
        else:
            return None

    @property
    def index(self):
        return self._index

    def seek(self, index):
        assert 0 <= index and index < len(self._lexemes)
        self._index = index
