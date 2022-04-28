_generator_registered_api = {}

def public_api(module):
    def inner(func):
        global _generator_registered_api
        if not module in _generator_registered_api:
            _generator_registered_api[module] = {}
        _generator_registered_api[module][func.__name__] = func
        return func
    return inner

def is_registered(module, func):
    global _generator_registered_api
    if module in _generator_registered_api:
        module = _generator_registered_api[module]
        return func in module
    return False
