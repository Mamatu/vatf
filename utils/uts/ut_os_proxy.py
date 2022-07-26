from unittest import TestCase
from unittest.mock import Mock

import logging
from vatf.utils import os_proxy

class OsProxyTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def test_join(self):
        self.assertEqual("a/b", os_proxy.join("a", "b"))
        self.assertEqual("a/b/c", os_proxy.join("a", "b/c"))
        self.assertEqual("a/b/c", os_proxy.join("a", os_proxy.join("b", "c")))
    def test_basename(self):
        self.assertEqual("c.txt", os_proxy.basename("a/b/c.txt"))
        self.assertEqual("c.txt", os_proxy.basename(os_proxy.join("a", "b", "c.txt")))
    def test_dirname(self):
        self.assertEqual("a/b", os_proxy.dirname("a/b/c.txt"))
        self.assertEqual("a/b", os_proxy.dirname(os_proxy.join("a", "b", "c.txt")))
