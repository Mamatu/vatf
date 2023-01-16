__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf.vatf_api import public_api

@public_api("bar")
def foo(a, b):
    pass

@public_api("bar")
def foo1(a):
    pass

@public_api("bar")
def foo2(path = '/tmp'):
    pass
