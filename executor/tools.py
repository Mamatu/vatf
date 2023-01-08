__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

@vatf_api.public_api("tools")
def copy(path, path_to_data):
    """
    Copy tools folder into destination path.
    @path - destination path
    @path_to_data - path to data for scripts
    """
    tools_rel_path = "../tools"
    scripts = ["convert_all_pcm_to_ogg.sh"]
    scripts = [os.path.join(tools_rel_path, s) for s in scripts]
    import shutil
    for s in scripts:
        shutil.copy(s, path)

@vatf_api.public_api("tools")
def copy_from_config(**kwargs):
    """
    Copy tools folder into destination path.
    @path - destination path
    @path_to_data - path to data for scripts
    """
    tools_rel_path = "../tools"
    scripts = ["convert_all_pcm_to_ogg.sh"]
    scripts = [os.path.join(tools_rel_path, s) for s in scripts]
    import shutil
    for s in scripts:
        shutil.copy(s, path)
