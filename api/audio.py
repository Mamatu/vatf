__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("audio")

def record_inputs_outputs():
    utils.print_func_info()
    _get_api().record_inputs_outputs()

def record_inputs_outputs_from_config(**kwargs):
    utils.print_func_info()
    _get_api().record_inputs_outputs_from_config(**kwargs)

def stop():
    utils.print_func_info()
    _get_api().stop()
