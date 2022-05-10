from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch
import sys

import logging
import textwrap
from vatf.generator import gen_tests

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
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    @patch("vatf.utils.os_proxy.mkdir")
    @patch("vatf.utils.os_proxy.open_to_read")
    @patch("vatf.utils.os_proxy.open_to_write")
    @patch("vatf.utils.os_proxy.copy")
    @patch("vatf.generator.gen_tests._create_run_sh_script")
    @patch("vatf.generator.gen_tests._create_header")
    def test_create_test(self, create_run_sh_script, create_header, os_proxy_copy, os_proxy_open_to_write, os_proxy_open_to_read, os_proxy_mkdir, os_proxy_write_to_file, is_registered, json_dump):
        with patch.object(sys, 'argv', ['', '', 'generator/tests/config.json']):
            is_registered.return_value = True
            create_run_sh_script = Mock()
            create_header = Mock()
            def test_body():
                bar.foo('a', 1)
                bar.foo(2)
                bar.foo(path = '/tmp')
            gen_tests.create_test("/tmp/", "test1", test_body)
            #os_proxy_open_to_write.assert_has_calls([call("/tmp/test1/test.py"), call("/tmp/test1/run_test.sh")])
            os_proxy_mkdir.assert_has_calls([call("/tmp/test1"), call("/tmp/test1/assets"), call("/tmp/test1/assets/audio_files")])
            expected_calls = []
            expected_calls.append(call(ANY, "bar.foo('a', 1)\n"))
            expected_calls.append(call(ANY, "bar.foo(2)\n"))
            expected_calls.append(call(ANY, "bar.foo(path = '/tmp')\n"))
            os_proxy_write_to_file.assert_has_calls(expected_calls)
