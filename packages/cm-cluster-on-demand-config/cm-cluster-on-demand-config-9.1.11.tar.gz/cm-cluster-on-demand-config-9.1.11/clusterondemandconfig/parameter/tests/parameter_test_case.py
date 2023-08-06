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

import copy
import unittest
from contextlib import contextmanager

import six

from clusterondemandconfig.exceptions import ConfigConstructError
from clusterondemandconfig.parser_utils import boolean_parser


class ParameterTestCase(unittest.TestCase):
    __test__ = False

    @contextmanager
    def assertRaisesTypeError(self, attr, actual, expected):
        expected = ", ".join(expected) if isinstance(expected, list) else expected
        be_one_of = "be one of" if "," in expected else "be"
        expected_message = ".*{attr} has invalid type {actual}, should {be_one_of} {expected}".format(
            attr=attr, actual=actual, be_one_of=be_one_of, expected=expected
        )
        with self.assertRaisesRegexp(ConfigConstructError, expected_message):
            yield

    def test_constructor_raises_if_name_is_not_a_string(self):
        with self.assertRaisesTypeError(".name", actual="int", expected=["str"]):
            self.subject_factory(name=1)

    def test_constructor_raises_if_name_is_not_valid_identifier(self):
        with self.assertRaisesRegexp(ConfigConstructError, r"1.name \(= '1'\) must match regex"):
            self.subject_factory(name="1")

    def test_constructor_raises_if_default_is_not_instance_of_type(self):
        with self.assertRaisesRegexp(ConfigConstructError, "some_parameter.default .* is not of type int"):
            self.subject_factory("some_parameter", default="bar", type=int)

    def test_constructor_raises_if_help_is_not_a_string(self):
        with self.assertRaisesTypeError(".help", actual="int", expected=["str"]):
            self.subject_factory("some_parameter", help=1)

    def test_constructor_raises_if_help_is_none(self):
        with self.assertRaisesTypeError(".help", actual="NoneType", expected=["str"]):
            self.subject_factory("some_parameter", help=None)

    def test_constructor_raises_if_help_section_is_not_a_string(self):
        with self.assertRaisesTypeError(".help_section", actual="int", expected=["str", "None"]):
            self.subject_factory("some_parameter", help_section=1)

    def test_constructor_raises_if_key_is_not_a_string(self):
        with self.assertRaisesTypeError(".key", actual="int", expected=["str", "None"]):
            self.subject_factory("some_parameter", key=1)

    def test_constructor_raises_if_key_is_not_a_valid_identifier(self):
        with self.assertRaisesRegexp(ConfigConstructError, r"some_parameter.key \(= '1'\) does not match regex"):
            self.subject_factory("some_parameter", key="1")

    def test_constructor_raises_if_parser_is_not_a_function_that_takes_a_single_argument(self):
        def bad_parser(a, b):
            pass

        with self.assertRaisesRegexp(ConfigConstructError, "some_parameter.parser .* must have arity of 1"):
            self.subject_factory("some_parameter", parser=bad_parser)

    def test_constructor_raises_if_serializer_is_not_a_function_that_takes_a_single_argument(self):
        def bad_serializer(a, b):
            pass

        with self.assertRaisesRegexp(ConfigConstructError, "some_parameter.serializer .* must have arity of 1"):
            self.subject_factory("some_parameter", serializer=bad_serializer)

    def test_constructor_raises_if_validation_is_not_a_list_of_functions(self):
        with self.assertRaisesTypeError(
                ".validation",
                actual=r"list\(\[int\]\)",
                expected=["function", r"list\(\[function\]\)", "None"]
        ):
            self.subject_factory("some_parameter", validation=[1, 2])

    def test_constructor_raises_if_validation_is_not_a_function_that_takes_a_two_argument(self):
        def bad_validation(a):
            pass

        with self.assertRaisesRegexp(ConfigConstructError, "some_parameter.validation .* must have arity of 2"):
            self.subject_factory("some_parameter", validation=[bad_validation])

    def test_constructor_completion_with_help_varname_set(self):
        subject = self.subject_factory("some_parameter", help_varname="SOME_VARNAME")

        self.assertEqual(subject.help_varname, "SOME_VARNAME")

    def test_constructor_completion_with_help_varname_and_type_set(self):
        subject = self.subject_factory("some_parameter", help_varname="SOME_VARNAME", type=bool)

        self.assertEqual(subject.help_varname, "SOME_VARNAME")

    def test_constructor_completion_with_whitespace_at_begin_and_end_of_in_help_text(self):
        subject = self.subject_factory("some_parameter", help=" foo ")

        self.assertEqual(subject.help, "foo.")

    def test_constructor_completion_without_dot_at_the_end_of_help_text(self):
        subject = self.subject_factory("some_parameter", help="bar")

        self.assertEqual(subject.help, "bar.")

    def test_constructor_completion_with_type_set(self):
        subject = self.subject_factory("some_parameter", type=bool)

        self.assertEqual(subject.type, bool)
        self.assertEqual(subject.parser, boolean_parser)

    def test_constructor_completion_with_parser_set(self):
        subject = self.subject_factory("some_parameter", parser=boolean_parser)

        self.assertEqual(subject.parser, boolean_parser)

    def test_copy_creates_a_near_identical_copy(self):
        subject = self.subject_factory("some_parameter")

        self.assertEqual(
            {k: v for (k, v) in six.iteritems(subject.__dict__) if "parent" != k},
            {k: v for (k, v) in six.iteritems(copy.copy(subject).__dict__) if "parent" != k}
        )

    def test_copy_sets_the_parent_of_the_clone(self):
        subject = self.subject_factory("some_parameter")

        self.assertEqual(subject, copy.copy(subject).parent)

    def test_ancestor_returns_self_if_subject_has_no_parent(self):
        subject = self.subject_factory("some_parameter")

        self.assertEqual(subject, subject.ancestor)

    def test_ancestor_returns_ancestor_of_parent_if_subject_has_parent(self):
        subject = self.subject_factory("some_parameter")

        self.assertEqual(subject.ancestor, copy.copy(subject).ancestor)

    def test_default_can_be_a_function(self):
        def default_method(parameter, configuration):
            pass

        self.subject_factory("some_parameter", default=default_method)

    def test_constructor_raises_if_default_function_takes_wrong_number_of_arguments(self):
        def bad_default_method(parameter, configuration, third_parameter):
            pass

        with self.assertRaisesRegexp(ConfigConstructError, "some_parameter.default .* must have arity of 2"):
            self.subject_factory("some_parameter", default=bad_default_method)
