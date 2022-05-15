from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch

import logging
import textwrap
from vatf.generator import mkdir

class MkdirTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("vatf.vatf_api.is_registered")
    @patch("vatf.generator.gen_tests.verify_call")
    def test_mkdir(self, verify_call, is_registered):
        is_registered.return_value = True
        mkdir.mkdir("/tmp/session")
        verify_call.assert_has_calls([call("mkdir.mkdir('/tmp/session')")])
    @patch("vatf.vatf_api.is_registered")
    @patch("vatf.generator.gen_tests.verify_call")
    def test_mkdir_with_counter(self, verify_call, is_registered):
        is_registered.return_value = True
        mkdir.mkdir_with_counter("/tmp/session")
        verify_call.assert_has_calls([call("mkdir.mkdir_with_counter('/tmp/session')")])
