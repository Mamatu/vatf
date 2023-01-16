def binary_search(array, is_lower, is_greater, index_and_value = False):
    def _binary_search(array, is_lower, is_greater, index_and_value, offset = 0):
        if len(array) == 0:
            return None
        if len(array) == 1:
            if index_and_value:
                return (offset, array[0])
            return array[0]
        _lend2 = int(len(array) / 2)
        v = array[_lend2]
        is_g = is_greater(v)
        is_l = is_lower(v)
        if is_g and is_l:
            raise Exception("Wrong is_lower and is_greater conditions")
        if not is_g and not is_l:
            if index_and_value:
                return (offset + _lend2, v)
            return v
        elif is_l:
            return _binary_search(array[_lend2 : len(array)], is_lower, is_greater, index_and_value = index_and_value, offset = _lend2 + offset)
        elif is_g:
            return _binary_search(array[0 : _lend2], is_lower, is_greater, index_and_value = index_and_value, offset = offset)
    return _binary_search(array, is_lower, is_greater, index_and_value, offset = 0)
