import logging
from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch
from vatf.generator import gen_tests
from vatf.vatf_api import public_api

import textwrap
import sys

from vatf.generator.tests import bar, bar_api

class GenTestsTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def test_make_pycall(self):
        self.assertEqual("foo()", gen_tests.make_pycall("foo"))
        self.assertEqual("foo('a')", gen_tests.make_pycall("foo", "a"))
        self.assertEqual("foo(a = 'a')", gen_tests.make_pycall("foo", a = "a"))
        self.assertEqual("foo('a', a = 'a')", gen_tests.make_pycall("foo", "a", a = "a"))
        self.assertEqual("foo('a', 1, a = 'a', b = 2)", gen_tests.make_pycall("foo", "a", 1, a = "a", b = 2))
        self.assertEqual("foo('a', 1, ('c', 'd'), a = 'a', b = 2)", gen_tests.make_pycall("foo", "a", 1, ("c", "d"), a = "a", b = 2))
        self.assertEqual("foo('a', 1, ('c', 'd'), a = 'a', b = 2, c = {'e': 9, 'f': 10})", gen_tests.make_pycall("foo", "a", 1, ("c", "d"), a = "a", b = 2, c = {"e": 9, "f": 10}))
    @patch("json.dump")
    @patch("vatf.vatf_api.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    @patch("vatf.utils.os_proxy.mkdir")
    @patch("vatf.utils.os_proxy.open_to_read")
    @patch("vatf.utils.os_proxy.open_to_write")
    @patch("vatf.utils.os_proxy.copy")
    @patch("vatf.generator.gen_tests._create_run_sh_script")
    @patch("vatf.generator.gen_tests._create_header")
    @patch("vatf.generator.gen_tests.verify_call")
    def test_create_test(self, verify_call, create_run_sh_script, create_header, os_proxy_copy, os_proxy_open_to_write, os_proxy_open_to_read, os_proxy_mkdir, os_proxy_write_to_file, is_registered, json_dump):
        with patch.object(sys, 'argv', ['', '', 'generator/tests/config.json']):
            is_registered.return_value = True
            create_run_sh_script = Mock()
            create_header = Mock()
            def test_body():
                bar_api.foo('a', 1)
                bar_api.foo1(2)
                bar_api.foo2(path = '/tmp')
            gen_tests.create_test("/tmp/", "test1", test_body)
            os_proxy_mkdir.assert_has_calls([call("/tmp/test1"), call("/tmp/test1/assets"), call("/tmp/test1/assets/audio_files")])
            expected_calls = []
            expected_calls.append(call("bar.foo('a', 1)"))
            expected_calls.append(call("bar.foo1(2)"))
            expected_calls.append(call("bar.foo2(path = '/tmp')"))
            verify_call.assert_has_calls(expected_calls)
