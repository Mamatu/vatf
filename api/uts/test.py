import logging
from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch
from vatf.utils import utils, os_proxy
from vatf.generator import gen_tests

import textwrap
import sys
import os

class TestTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)
    def test_test_suite_api(self):
        test_folder = ["assets", "config.json", "run_test.sh", "test.py"]
        suite_path = utils.get_temp_file()
        logging.debug(f"suite_path: {suite_path}")
        os.system(f"./python.sh api/tests/test_suite_api.py {suite_path} ./api/tests/config.json ./api/tests/custom.json")
        self.assertEqual(2, len(os_proxy.listdir(suite_path)))
        for file in test_folder:
            self.assertTrue(os_proxy.exists(f"{suite_path}/Test_1/{file}"))
            self.assertTrue(os_proxy.exists(f"{suite_path}/Test_2/{file}"))
        test_py_header = gen_tests.get_test_py_header(["config.json", "custom.json"])
        with open(f"{suite_path}/Test_1/test.py","r") as test_file:
            lines = test_file.readlines()
            for idx in range(len(test_py_header)):
                header_line = test_py_header[idx].format(branch = "")
                self.assertEqual(f"{header_line}\n", lines[idx])
            test_code = lines[len(test_py_header):]
            self.assertEqual("print(\"set_up\")\n", test_code[0])
            self.assertEqual("print(\"Test_1\")\n", test_code[1])
            self.assertEqual("print(\"tear_down\")\n", test_code[2])
        with open(f"{suite_path}/Test_2/test.py","r") as test_file:
            lines = test_file.readlines()
            for idx in range(len(test_py_header)):
                header_line = test_py_header[idx].format(branch = "")
                self.assertEqual(f"{header_line}\n", lines[idx])
            test_code = lines[len(test_py_header):]
            self.assertEqual("print(\"set_up\")\n", test_code[0])
            self.assertEqual("print(\"Test_2\")\n", test_code[1])
            #print(test_code[2])
            #self.assertTrue("wait.sleep(1)\n" == test_code[2] or "wait.sleep(2)\n" == test_code[2])
            self.assertEqual("print(\"tear_down\")\n", test_code[3])
