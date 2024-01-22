import os
import pathlib
import shutil

from vatf.utils import config_handler

def create_tools_dir_form_config(**kwargs):
    tools_pathes_key = "tools.pathes"
    config = config_handler.get_config(**kwargs)
    pathes = None
    try:
        pathes = config[tools_pathes_key]
    except KeyError:
        pass
    if isinstance(pathes, str):
        pathes = [pathes]
    tools_path = pathlib.Path(__file__).parent.parent.resolve()
    tools_path = os.path.join(tools_path, "tools")
    files = os.listdir(tools_path)
    for path in pathes:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok = True)
        templates_path = os.path.join(path, "tools/.templates")
        if not os.path.exists(templates_path):
            os.makedirs(templates_path, exist_ok = True)
        for file in files:
            dir_file = os.path.join(tools_path, file)
            shutil.copy(dir_file, templates_path)
            if file in _scripts.keys():
                _scripts[file](path)

def _create_convert_all_pcm_to_ogg(path):
    with open(os.path.join(path, "tools/convert_all_pcm_to_ogg.sh"), "w") as f:
        f.write("WORKSPACE_PATH=.. bash ./.templates/template.convert_all_pcm_to_ogg.sh")

_scripts = {"template.convert_all_pcm_to_ogg.sh" : _create_convert_all_pcm_to_ogg}
