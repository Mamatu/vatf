import importlib

class Loader:
    _fields = ["vatf", "assets", "va_log", "audio", "utterance_to_va", "utterance_from_va"]
    def __init__(self, path):
        self.variables = self._load_config(path)
    def _load_config(self, path):
        variables = {}
        import os.path
        module = importlib.import_module(package = os.path.dirname(path), name = os.path.basename(path))
        for f in _fields:
            variables[f] = getattr(module, f)
        return variables
    def __getattr__(self, attr):
        class Wrapper:
            def __init__(self, attr):
                self.attr = attr
            def __getattr__(self, attr):
                if isinstance(self.attr, dict):
                    if attr in self.attr:
                        return self.attr[attr]
                    else:
                        raise AttributeError
        if attr  in self.variables:
            return Wrapper(self.variables[attr])
        else:
            raise AttributeError
