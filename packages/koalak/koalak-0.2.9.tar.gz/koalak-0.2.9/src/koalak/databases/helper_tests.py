"""These class are here to help unitesting the database classes"""
import os
import typing
from typing import List

import pytest
from koalak.utils import get_prefixed_callables_of_object, temp_pathname

from .databases import ListDB


class HelperTest:
    def test(self):
        for test_method in get_prefixed_callables_of_object(self, "test_"):
            test_method()


class HelperTestListDatabase(HelperTest):
    def __init__(self, cls: typing.Type[ListDB], values: List = None):
        if values is None:
            values = [1, 2, 3, "c", True, [], {}]

        self.cls = cls
        self.values = values

        # Values to test with must be at least 3
        assert len(self.values) >= 3

        # Must be unique
        # convert to string so that we can transform our list into set
        #  because dict can not be hashable
        tmp_values = [str(e) for e in self.values]
        assert len(set(tmp_values)) == len(self.values)

        # The first three element must be sorted
        assert self.values[:3] == sorted(self.values[:3])

    def test_simple(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as path:
            l = self.cls(path)

            l.append(v1)

            assert len(l) == 1
            assert l[0] == v1
            assert list(l) == [v1]
            assert l.count(v1) == 1

            # Retest without append
            l = self.cls(path)
            assert len(l) == 1
            assert l[0] == v1
            assert list(l) == [v1]
            assert l.count(v1) == 1

            # Modify it
            l = self.cls(path)
            l[0] = v2

            l = self.cls(path)
            assert l[0] == v2

    def test__add_radd(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as path:
            l = self.cls(path, [v1], autosync=True)
            l2 = l + [v2]

            assert l2 == [v1, v2]
            assert type(l2) is list
            assert list(l) == [v1]

            l3 = [v2] + l
            assert l3 == [v2, v1]
            assert type(l3) is list
            assert list(l) == [v1]

    def test__del(self):

        v1, v2, v3 = self.values[:3]

        with temp_pathname() as path:

            l = self.cls(path, [v1, v2, v3], autosync=True)
            assert list(l) == [v1, v2, v3]

            del l[0]
            assert list(l) == [v2, v3]
            l = self.cls(path, autosync=True)
            assert list(l) == [v2, v3]

    def test__getitem(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as path:
            l = self.cls(path, [v1, v2, v3], autosync=True)
            assert list(l) == [v1, v2, v3]

            assert l[0] == v1
            assert l[-1] == v3

            assert l[:] == [v1, v2, v3]
            assert type(l[:]) is list
            assert type(l[:2]) is list  # and not DBList
            assert l[:2] == [v1, v2]

    def test_pop(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as path:
            l = self.cls(path, [v1, v2, v3], autosync=True)
            l.pop()
            assert l == [v1, v2]
            l = self.cls(path, autosync=True)
            assert l == [v1, v2]

            l.pop(0)
            assert l == [v2]
            l = self.cls(path, autosync=True)
            assert l == [v2]

    def test__mul_rmul(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as path:
            l = self.cls(path, [v1], autosync=True)
            l2 = l * 2

            assert l2 == [v1, v1]
            assert type(l2) is list
            assert list(l) == [v1]

            l3 = 2 * l
            assert l3 == [v1, v1]
            assert type(l3) is list
            assert list(l) == [v1]

    def test_count(self):
        v1 = self.values[0]
        v2 = self.values[1]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            l.append(v1)

            assert l.count(v1) == 1
            l = self.cls(dbpath, autosync=True)
            assert l.count(v1) == 1

            l.append(v2)
            l.append(v1)
            assert l.count(v1) == 2
            assert l.count(v2) == 1

            l = self.cls(dbpath, autosync=True)
            assert l.count(v1) == 2
            assert l.count(v2) == 1

    def test_index(self):
        v1 = self.values[0]
        v2 = self.values[1]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            l.append(v1)
            l.append(v2)

            assert l.index(v1) == 0
            assert l.index(v2) == 1

            l = self.cls(dbpath, autosync=True)
            assert l.index(v1) == 0
            assert l.index(v2) == 1

            # example with start/stop
            assert l.index(v2, 1) == 1
            assert l.index(v1, 0, 2) == 0

    def test_autosync(self):
        v1 = self.values[0]
        v2 = self.values[1]
        v3 = self.values[2]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            l.append(v1)

            # append
            l = self.cls(dbpath, autosync=True)
            assert l[0] == v1

            # remove
            l.remove(v1)
            l = self.cls(dbpath, autosync=True)
            assert len(l) == 0

            # test extend
            l.extend(self.values[:3])  # extend the 3 first elements
            l = self.cls(dbpath, autosync=True)
            assert len(l) == 3
            assert list(l) == self.values[:3]

            # test clear
            l.clear()
            l = self.cls(dbpath, autosync=True)
            assert list(l) == []

            # test insert
            l.clear()
            l.append(v2)
            l.insert(0, v1)
            assert list(l) == [v1, v2]
            l = self.cls(dbpath, autosync=True)
            assert list(l) == [v1, v2]

            # test pop
            l.clear()
            l.append(v1)
            l.append(v2)
            assert l.pop(0) == v1
            assert l.pop(0) == v2
            assert list(l) == []
            l = self.cls(dbpath, autosync=True)
            assert list(l) == []

            # test reverse
            l.clear()
            l.append(v1)
            l.append(v2)
            l.append(v3)
            l.reverse()
            assert list(l) == [v3, v2, v1]
            l = self.cls(dbpath, autosync=True)
            assert list(l) == [v3, v2, v1]

            # test sort
            l.clear()
            l.append(v2)
            l.append(v3)
            l.append(v1)
            l.sort()
            assert list(l) == [v1, v2, v3]
            l = self.cls(dbpath, autosync=True)
            assert list(l) == [v1, v2, v3]

    def test_contains(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            assert "a" not in l
            assert "b" not in l

            l.append("a")
            assert "a" in l
            l = self.cls(dbpath, autosync=True)
            assert "a" in l

            l.append("b")
            assert "a" in l
            assert "b" in l
            assert "c" not in l
            l = self.cls(dbpath, autosync=True)
            assert "a" in l
            assert "b" in l
            assert "c" not in l

            l.append("c")
            assert "a" in l
            assert "b" in l
            assert "c" in l
            l = self.cls(dbpath, autosync=True)
            assert "a" in l
            assert "b" in l
            assert "c" in l

            l.remove("a")
            assert "a" not in l
            l = self.cls(dbpath, autosync=True)
            assert "a" not in l

    def test_file_is_created(self):
        """Assert that the file is created in the constructor"""
        with temp_pathname() as dbpath:
            self.cls(dbpath, autosync=True)
            assert os.path.exists(dbpath)

    def test_initiated_with_existing_list(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, [v1, v2, v3], autosync=True)
            assert list(l) == [v1, v2, v3]
            l = self.cls(dbpath, autosync=True)
            assert list(l) == [v1, v2, v3]

            l.remove(v1)
            assert list(l) == [v2, v3]

            l = self.cls(dbpath, autosync=True)
            assert list(l) == [v2, v3]

    def test_conflict_args_obj_and_existing_db(self):
        v1, v2, v3 = self.values[:3]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)  # the file dbpath is created
            with pytest.raises(TypeError):
                # once the file is created we can't initiate it with an existing list
                l = [v1, v2, v3]
                self.cls(dbpath, l, autosync=True)

    def test_double_sync(self):
        """Test that double sync is possible"""
        v1, v2, v3 = self.values[:3]
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            l.append(v1)
            l.sync()
            l.sync()

    def test_nb_sync(self):
        v1, v2, v3 = self.values[:3]
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            nb_sync = l._nb_sync
            l.append(v1)  # sync called here
            l.sync()  # this sync is useless because already synced
            assert l._nb_sync == nb_sync + 1  # check that the previous sync did nothing
            l.extend([v1, v1, v1])
            assert (
                l._nb_sync == nb_sync + 2
            )  # check that extend call sync once and not 3 time

    def test_unique(self):
        v1, v2, v3 = self.values[:3]

        # test append
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            with pytest.raises(ValueError):
                l.append("a")

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l.append("a")

        # test insert
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            with pytest.raises(ValueError):
                l.insert(0, "a")

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l.insert(0, "a")

        # test extend
        with temp_pathname() as dbpath:
            # FIXME: if error occure on extend we don't validate first elem?
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            with pytest.raises(ValueError):
                l.extend(["b", "a"])

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l.extend(["b", "a"])

        with temp_pathname() as dbpath:
            # FIXME: if error occure on extend we don't validate first elem?
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            with pytest.raises(ValueError):
                l.extend(["b", "b"])

            l = self.cls(dbpath, autosync=True, unique=True)

        # test setitem
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            l.append("b")
            with pytest.raises(ValueError):
                l[1] = "a"

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l[1] = "a"

            assert list(l) == ["a", "b"]
            # it is allowed to modify the same value
            l[0] = "a"

    def test_unique_as_function(self):
        v1, v2, v3 = self.values[:3]

        # test append
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=lambda x: x.split("=")[0])

            l.append("a=1")
            l.append("b=2")
            l.append("c=3")
            assert list(l) == ["a=1", "b=2", "c=3"]
            l = self.cls(dbpath, autosync=True, unique=lambda x: x.split("=")[0])
            assert list(l) == ["a=1", "b=2", "c=3"]

            with pytest.raises(ValueError):
                l.append("a=5")


class HelperTestDictDB(HelperTest):
    def __init__(
        self, cls: typing.Type[ListDB], values: List = None, keys: List[str] = None
    ):
        if values is None:
            values = [1, 2, 3, "c", True, [], {}]

        if keys is None:
            keys = ["a", "b", "c"]
        self.cls = cls
        self.values = values
        self.keys = keys

        # Values to test with must be at least 3
        assert len(self.values) >= 3
        assert len(self.keys) >= 3
        # Must be unique
        # convert to string so that we can transform our list into set
        #  because dict can not be hashable
        tmp_values = [str(e) for e in self.values]
        assert len(set(tmp_values)) == len(self.values)

        tmp_keys = [str(e) for e in self.keys]
        assert len(set(tmp_keys)) == len(self.keys)

        # The first three element must be sorted
        assert self.values[:3] == sorted(self.values[:3])
        assert self.keys[:3] == sorted(self.keys[:3])

    def test_simple(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]

        with temp_pathname() as path:
            l = self.cls(path, autosync=True)

            l[k1] = v1

            assert len(l) == 1
            assert l[k1] == v1
            assert list(l) == [k1]
            assert dict(l) == {k1: v1}

            # Retest without append
            l = self.cls(path, autosync=True)
            assert len(l) == 1
            assert l[k1] == v1
            assert list(l) == [k1]
            assert dict(l) == {k1: v1}

            # Modify it
            l = self.cls(path, autosync=True)
            l[k1] = v2
            assert dict(l) == {k1: v2}

            l = self.cls(path, autosync=True)
            assert dict(l) == {k1: v2}
            assert l[k1] == v2

    def test__del(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]
        print()
        print("entering test__del")

        with temp_pathname() as path:
            print("path", path, os.path.exists(path))
            d = self.cls(path, {k1: v1, k2: v2, k3: v3}, autosync=True)
            print("temp_path: after init path", path, os.path.exists(path))
            assert dict(d) == {k1: v1, k2: v2, k3: v3}

            del d[k1]
            assert dict(d) == {k2: v2, k3: v3}
            print("test__del:temp_path: containt path", open(path).read())
            d = self.cls(path, autosync=True)
            assert dict(d) == {k2: v2, k3: v3}

    def test__getitem(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]

        with temp_pathname() as path:
            l = self.cls(path, {k1: v1, k2: v2, k3: v3}, autosync=True)
            assert dict(l) == {k1: v1, k2: v2, k3: v3}

            assert l[k1] == v1
            assert l[k3] == v3

            assert dict(l) == {k1: v1, k2: v2, k3: v3}
            assert list(l) == [k1, k2, k3]

    def test_autosync(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            l[k1] = v1

            l = self.cls(dbpath, autosync=True)
            assert l[k1] == v1

            # delete
            del l[k1]
            l = self.cls(dbpath, autosync=True)
            assert len(l) == 0

    def test_contains(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            assert k1 not in l
            assert k2 not in l

            l[k1] = v1
            assert k1 in l
            l = self.cls(dbpath, autosync=True)
            assert k1 in l

            l[k2] = v2
            assert k1 in l
            assert k2 in l
            assert k3 not in l
            l = self.cls(dbpath, autosync=True)
            assert k1 in l
            assert k2 in l
            assert k3 not in l

            l[k3] = v3
            assert k1 in l
            assert k2 in l
            assert k3 in l
            l = self.cls(dbpath, autosync=True)
            assert k1 in l
            assert k2 in l
            assert k3 in l

            del l[k1]
            assert k1 not in l
            l = self.cls(dbpath, autosync=True)
            assert k1 not in l

    def test_file_is_created(self):
        """Assert that the file is created in the constructor"""
        with temp_pathname() as dbpath:
            self.cls(dbpath, autosync=True)
            assert os.path.exists(dbpath)

    def test_initiated_with_existing_dict(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, {k1: v1, k2: v2, k3: v3}, autosync=True)
            assert dict(l) == {k1: v1, k2: v2, k3: v3}
            l = self.cls(dbpath, autosync=True)
            assert dict(l) == {k1: v1, k2: v2, k3: v3}

            del l[k1]
            assert dict(l) == {k2: v2, k3: v3}

            l = self.cls(dbpath, autosync=True)
            assert dict(l) == {k2: v2, k3: v3}

    def test_conflict_args_obj_and_existing_db(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]

        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)  # the file dbpath is created
            with pytest.raises(TypeError):
                # once the file is created we can't initiate it with an existing list
                l = {k1: v1, k2: v2, k3: v3}
                self.cls(dbpath, l, autosync=True)

    def test_double_sync(self):
        """Test that double sync is possible"""
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            l[k1] = v1
            l.sync()
            l.sync()

    def test_nb_sync(self):
        v1, v2, v3 = self.values[:3]
        k1, k2, k3 = self.keys[:3]
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True)
            nb_sync = l._nb_sync
            l[k1] = v1  # sync called here
            l.sync()  # this sync is useless because already synced
            assert l._nb_sync == nb_sync + 1  # check that the previous sync did nothing
            l.update({k2: v2, k3: v3})
            assert (
                l._nb_sync == nb_sync + 2
            )  # check that extend call sync once and not 3 time

    def notttest_unique(self):
        v1, v2, v3 = self.values[:3]

        # test append
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=True)
            l[k1] = v1

            with pytest.raises(ValueError):
                l[k2] = v1

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l.append("a")

        # test insert
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            with pytest.raises(ValueError):
                l.insert(0, "a")

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l.insert(0, "a")

        # test extend
        with temp_pathname() as dbpath:
            # FIXME: if error occure on extend we don't validate first elem?
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            with pytest.raises(ValueError):
                l.extend(["b", "a"])

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l.extend(["b", "a"])

        with temp_pathname() as dbpath:
            # FIXME: if error occure on extend we don't validate first elem?
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            with pytest.raises(ValueError):
                l.extend(["b", "b"])

            l = self.cls(dbpath, autosync=True, unique=True)

        # test setitem
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=True)

            l.append("a")
            l.append("b")
            with pytest.raises(ValueError):
                l[1] = "a"

            l = self.cls(dbpath, autosync=True, unique=True)

            with pytest.raises(ValueError):
                l[1] = "a"

            assert list(l) == ["a", "b"]
            # it is allowed to modify the same value
            l[0] = "a"

    def nottest_unique_as_function(self):
        v1, v2, v3 = self.values[:3]

        # test append
        with temp_pathname() as dbpath:
            l = self.cls(dbpath, autosync=True, unique=lambda x: x.split("=")[0])

            l.append("a=1")
            l.append("b=2")
            l.append("c=3")
            assert list(l) == ["a=1", "b=2", "c=3"]
            l = self.cls(dbpath, autosync=True, unique=lambda x: x.split("=")[0])
            assert list(l) == ["a=1", "b=2", "c=3"]

            with pytest.raises(ValueError):
                l.append("a=5")
