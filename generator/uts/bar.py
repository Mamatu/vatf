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
