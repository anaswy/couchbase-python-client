from time import sleep

from couchbase import FMT_JSON, FMT_PICKLE, FMT_UTF8, FMT_BYTES
from couchbase.exceptions import (KeyExistsError, ValueFormatError,
                                  ArgumentError, NotFoundError,
                                  NotStoredError)

from tests.base import CouchbaseTestCase

#
# Copyright 2013, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
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
#

class ConnectionBadArgsTest(CouchbaseTestCase):
    def setUp(self):
        super(ConnectionBadArgsTest, self).setUp()
        self.cb = self.make_connection()

    def test_bad_single(self):

        for k in (
            (),
            ("key",),
            {"key":"value"},
            [],
            set(),
            {}.keys(),
            {}.values(),
            ["key"],
            None,
            True,
            False,
            0,
            object()):

            print("Testing with key (%r)" % (k,))

            self.assertRaises(ValueFormatError, self.cb.get, k)
            self.assertRaises(ValueFormatError, self.cb.incr, k)
            self.assertRaises(ValueFormatError, self.cb.delete, k)
            self.assertRaises(ValueFormatError, self.cb.set, k, "value")
            self.assertRaises(ValueFormatError, self.cb.set, "key", k,
                              format=FMT_UTF8)
            self.assertRaises(ValueFormatError, self.cb.set, "key", k,
                              format=FMT_BYTES)
            self.assertRaises(ValueFormatError, self.cb.append, "key", k)

    def test_bad_multi(self):
        for k in (
            "key",
            None,
            [],
            {},
            set(),
            {}.keys(),
            {}.values(),
            0,
            object()):
            print("Testing with keys (%r)" % (k,))

            self.assertRaises(ArgumentError, self.cb.get_multi, k)
            self.assertRaises(ArgumentError, self.cb.set_multi, k)
            self.assertRaises(ArgumentError, self.cb.incr_multi, k)
            self.assertRaises(ArgumentError, self.cb.delete_multi, k)

    def test_bad_timeout(self):
        def _set_timeout(x):
            self.cb.timeout = x

        self.assertRaises(ValueError, _set_timeout, 0)
        self.assertRaises(ValueError, _set_timeout, -1)
        self.assertRaises(TypeError, _set_timeout, None)
        self.assertRaises(TypeError, _set_timeout, "a string")

        self.cb.timeout = 0.1
        self.cb.timeout = 1
        self.cb.timeout = 2.5

    def test_bad_quiet(self):
        def _set_quiet(x):
            self.cb.quiet = x

        self.assertRaises(Exception, _set_quiet, "asfasf")
        self.assertRaises(Exception, _set_quiet, None)
        _set_quiet(True)
        _set_quiet(False)

    def test_bad_default_format(self):
        def _set_fmt(x):
            self.cb.default_format = x
            self.assertEqual(self.cb.default_format, x)

        _set_fmt(FMT_JSON)
        _set_fmt(FMT_BYTES)
        _set_fmt(FMT_UTF8)
        _set_fmt(FMT_PICKLE)

        self.assertRaises(ArgumentError, _set_fmt, "a format")
        self.assertRaises(ArgumentError, _set_fmt, None)
        self.assertRaises(ArgumentError, _set_fmt, False)
        self.assertRaises(ArgumentError, _set_fmt, True)
        self.assertRaises(ArgumentError, _set_fmt, object())

        # TODO: Stricter format handling

        #self.assertRaises(ArgumentError, self.cb.set,
        #                  "foo", "bar", format=-1)



if __name__ == '__main__':
    unittest.main()
