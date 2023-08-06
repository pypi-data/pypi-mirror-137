import os

from koalak.utils import get_prefixed_callables_of_object, randomstr, temp_pathname


def test_randomstr():
    # By default the function work (no need the first param)
    randomstr()

    # test length
    for _ in range(20):
        assert len(randomstr(10)) == 10
        assert len(randomstr(20)) == 20

    # test alphabet
    alphabet = "abc"
    for _ in range(20):
        a = randomstr(alphabet=alphabet)
        for c in a:
            assert c in alphabet

    # test exclude
    alphabet = "ab"
    a = randomstr(1, alphabet=alphabet, exclude="a")
    assert a == "b"

    # test prefix
    for _ in range(20):
        assert randomstr(prefix="ab_").startswith("ab_")


def test_temp_pathname():
    # Test that if we create a file, it is correctly removed
    with temp_pathname() as pathname:
        saved_pathname = pathname
        assert not os.path.exists(pathname)
        # create the file
        open(pathname, "w")

        assert os.path.exists(pathname)
    assert not os.path.exists(saved_pathname)

    # Test that if we create a directory, it is correctly removed
    with temp_pathname() as pathname:
        saved_pathname = pathname
        assert not os.path.exists(pathname)
        # create the file
        os.makedirs(os.path.join(pathname, "test"))
        assert os.path.exists(pathname)
    assert not os.path.exists(saved_pathname)

    # Test that the file is correctly removed after an exception
    class DummyException(Exception):
        pass

    try:
        with temp_pathname() as pathname:
            # create the file
            open(pathname, "w")
            raise DummyException
    except DummyException:
        assert not os.path.exists(pathname)


def test_get_prefixed_callables_of_object():
    class A:
        test_nop = "something"

        def f(self):
            pass

        def test_a(self):
            pass

        def test_b(self):
            pass

    a = A()
    assert get_prefixed_callables_of_object(a, "test_") == [a.test_a, a.test_b]

    class B:
        test_nop = "something"
        run_z = "something"

        def f(self):
            pass

        def test_a(self):
            pass

        def test_b(self):
            pass

        def run_x(self):
            pass

        def run_y(self):
            pass

    b = B()
    assert get_prefixed_callables_of_object(b, "test_") == [b.test_a, b.test_b]
    assert get_prefixed_callables_of_object(b, "run_") == [b.run_x, b.run_y]
