_api = {}

def test_api(func):
    global _api
    _api[func.__name__] = func

def is_registered(func):
    global _api
    return func in _api
