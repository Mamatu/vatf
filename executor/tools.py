__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

@vatf_api.public_api("wait")
def copy(path, path_to_data):
    """
    Copy tools folder into destination path.
    @path - destination path
    @path_to_data - path to data for scripts
    """
    import shutil
    tools_rel_path = "../tools"
    shutil.copytree(tools_rel_path, path)
    
