_generator_registered_api = {}

def public_api(func):
    global _generator_registered_api
    _generator_registered_api[func.__name__] = func
    return func

def is_registered(func):
    global _generator_registered_api
    return func in _generator_registered_api
