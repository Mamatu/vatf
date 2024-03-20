__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf.utils import config_handler
from vatf.utils import libsampling

def start_from_config(**kwargs):
    config = config_handler.get_config(**kwargs)
    libsampling.process(config.sampling)
