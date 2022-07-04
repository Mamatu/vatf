from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("bar", custom_package = "vatf.generator.uts")

def foo(a, b):
   return  _get_api().foo(a, b)
    
def foo1(a):
   return  _get_api().foo1(a)

def foo2(path = '/tmp'):
   return  _get_api().foo2(path = path)
