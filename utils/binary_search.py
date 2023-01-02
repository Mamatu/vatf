def binary_search(array, is_lower, is_greater):
    if len(array) == 0:
        return None
    if len(array) == 1:
        return array[0]
    _lend2 = int(len(array) / 2)
    v = array[_lend2]
    is_g = is_greater(v)
    is_l = is_lower(v)
    if is_g and is_l:
        raise Exception("Wrong is_lower and is_greater conditions")
    if not is_g and not is_l:
        return v
    elif is_l:
        return binary_search(array[_lend2 : len(array)], is_lower, is_greater)
    elif is_g:
        return binary_search(array[0 : _lend2], is_lower, is_greater)

