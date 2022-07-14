from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("audio")

def record_inputs_outputs():
    _get_api().record_inputs_outputs()

def record_inputs_outputs_from_config(**kwargs):
    _get_api().record_inputs_outputs_from_config(**kwargs)
