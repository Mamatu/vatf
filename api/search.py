from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("search")

def find(filepath, regex, only_math = False):
    return _get_api().find(filepath, regex, only_match = only_match)

def find_in_line(filepath, grep_regex, match_regex):
    return _get_api().find_in_line(filepath, grep_regex, match_regex)
