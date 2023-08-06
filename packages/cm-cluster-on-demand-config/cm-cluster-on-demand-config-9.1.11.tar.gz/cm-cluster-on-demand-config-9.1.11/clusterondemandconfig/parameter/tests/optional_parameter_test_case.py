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

from clusterondemandconfig.exceptions import ConfigConstructError

from .parameter_test_case import ParameterTestCase


class OptionalParameterTestCase(ParameterTestCase):
    def test_constructor_raises_if_env_is_not_a_string_or_none(self):
        with self.assertRaisesTypeError(".env", actual="bool", expected=["str", "None"]):
            self.subject_factory("some_parameter", env=True)

    def test_constructor_raises_if_env_does_not_match_regexp(self):
        with self.assertRaisesRegexp(ConfigConstructError, r"some_parameter.env \(= 'env'\) does not match regex"):
            self.subject_factory("some_parameter", env="env")

    def test_constructor_raises_if_flags_is_not_a_list(self):
        with self.assertRaisesTypeError(".flags", actual="str", expected=[r"list\(\[str\]\)", "None"]):
            self.subject_factory("some_parameter", flags="--some-parameter")

    def test_constructor_raises_if_flag_is_not_a_string(self):
        with self.assertRaisesTypeError(".flags", actual=r"list\(\[int\]\)", expected=[r"list\(\[str\]\)", "None"]):
            self.subject_factory("some_parameter", flags=[1, 2])

    def test_constructor_raises_if_flag_is_not_a_valid_flag(self):
        with self.assertRaisesRegexp(ConfigConstructError, "some_parameter.flag __foo-bar does not match regex "):
            self.subject_factory("some_parameter", flags=["__foo-bar"])

    def test_constructor_completion_with_default_flag_already_in_flags(self):
        subject = self.subject_factory("some_parameter", flags=["--some-parameter", "-s"])

        self.assertEqual(subject.flags, ["-s"])
