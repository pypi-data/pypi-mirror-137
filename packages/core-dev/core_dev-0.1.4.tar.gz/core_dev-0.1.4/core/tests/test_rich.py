



from _core._rich import rich_exception_decorator

@rich_exception_decorator
def function(a=123):
    print(a)


def test_rich_exception_decorator():
    assert function() == None