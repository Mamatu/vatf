__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("bar", custom_package = "vatf.generator.uts")

def foo(a, b):
   return  _get_api().foo(a, b)
    
def foo1(a):
   return  _get_api().foo1(a)

def foo2(path = '/tmp'):
   return  _get_api().foo2(path = path)
