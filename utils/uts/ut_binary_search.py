from vatf.utils.binary_search import binary_search

def test_binary_search_1():
    assert None == binary_search([], lambda x: x < 5, lambda x: x > 5)

def test_binary_search_2():
    assert 2 == binary_search([1, 2, 3], lambda x: x < 2, lambda x: x > 2)

def test_binary_search_3():
    assert (1, 1) == binary_search([(1, 1), (2, 2), (3, 3)], lambda x: x[0] < 1, lambda x: x[0] > 1)

def test_binary_search_4():
    assert (2, 2) == binary_search([(1, 1), (2, 2), (3, 3)], lambda x: x[0] < 2, lambda x: x[0] > 2)

def test_binary_search_5():
    assert (3, 3) == binary_search([(1, 1), (2, 2), (3, 3)], lambda x: x[0] < 3, lambda x: x[0] > 3)

def test_binary_search_6():
    from datetime import datetime
    now = datetime(2022, 1, 29, 20, 54, 55, 570000)
    array = [(datetime(2022, 1, 29, 20, 54, 55, 567000), 1), (datetime(2022, 1, 29, 20, 54, 55, 567000), 2), (datetime(2022, 1, 29, 20, 54, 55, 568000), 3), (datetime(2022, 1, 29, 20, 54, 55, 569000), 4), (datetime(2022, 1, 29, 20, 54, 55, 570000), 5), (datetime(2022, 1, 29, 20, 54, 55, 600000), 6)]
    print(now)
    for a in array:
        if a[1] < 5:
            assert a[0] < now
        if a[1] == 5:
            assert a[0] == now
        if a[1] > 5:
            assert a[0] > now
    out = binary_search(array, lambda x: x[0] < now, lambda x: now < x[0])
    assert out[1] == 5
