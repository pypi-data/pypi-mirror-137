import tempfile

import pytest
from koalak.databases import JsonListDB, TxtListDB
from koalak.helpers_test import HelperTestListDatabase
from koalak.utils import temp_pathname


# ---------------- TEST ListJsonDatabase --------------- #
def test_with_helper_json_db():
    HelperTestListDatabase(JsonListDB).test()


def test_json_db_create_manual_db():
    with temp_pathname() as dbpath:
        with open(dbpath, "w") as f:
            f.write('["a", "b", 3]')
        l = JsonListDB(dbpath, autosync=True)
        assert list(l) == ["a", "b", 3]


def test_json_db_dict_instead_of_list_error():
    with temp_pathname() as dbpath:
        with open(dbpath, "w") as f:
            f.write("{}")
        with pytest.raises(TypeError):
            l = JsonListDB(dbpath, autosync=True)


# ---------------- TEST ListTxtDatabase --------------- #
def test_with_helper_txt_db():
    HelperTestListDatabase(TxtListDB, values=["a", "b", "c", "d", "e"]).test()


def test_txt_db_type():
    """Test that the DB only accept txt type"""
    with temp_pathname() as dbpath:
        l = TxtListDB(dbpath, autosync=False)
        l.append("a")
        l.sync()
        assert "a" in l

        l = TxtListDB(dbpath, autosync=False)
        assert "a" in l

        with pytest.raises(TypeError):
            l.append(123)

        with pytest.raises(TypeError):
            l.append(False)

        with pytest.raises(TypeError):
            l.insert(0, 123)

        with pytest.raises(TypeError):
            l.extend(["a", False])

        with pytest.raises(TypeError):
            l[0] = 50


def test_txt_db_no_newline():
    """Test that the DB don't accept newline"""
    with temp_pathname() as dbpath:
        l = TxtListDB(dbpath, autosync=True)
        l.append("a")
        assert "a" in l

        l = TxtListDB(dbpath, autosync=True)
        assert "a" in l

        with pytest.raises(ValueError):
            l.append("a\nb")


# TODO: test how json files are
def test_txt_db_filecontent():
    """Test how the file is inside"""
    with temp_pathname() as dbpath:
        l = TxtListDB(dbpath, autosync=True)

        l.append("a")
        assert "a" in l
        assert open(dbpath).read() == "a\n"

        l = TxtListDB(dbpath, autosync=True)
        assert open(dbpath).read() == "a\n"

        l.append("b")
        assert open(dbpath).read() == "a\nb\n"

        l.clear()
        assert open(dbpath).read() == ""

        l.append("a")
        l.append("b")
        assert open(dbpath).read() == "a\nb\n"

        l.remove("a")
        assert open(dbpath).read() == "b\n"


def test_txt_db_create_manual_db():
    with temp_pathname() as dbpath:
        with open(dbpath, "w") as f:
            f.write("a\nb\n")
        l = TxtListDB(dbpath, autosync=True)
        assert list(l) == ["a", "b"]
