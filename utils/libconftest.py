import pytest

def pytest_addhooks(pluginmanager):
    from vatf.utils import libhooks
    pluginmanager.register(libhooks)
