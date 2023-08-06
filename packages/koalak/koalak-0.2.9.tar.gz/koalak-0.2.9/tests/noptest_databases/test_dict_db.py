import tempfile

import pytest
from koalak.databases import JsonDictDB, TxtDictDB
from koalak.helpers_test import HelperTestDictDB
from koalak.utils import temp_pathname


# ---------------- TEST JsonDictDB --------------- #
def test_jsondictdb_with_helper():
    HelperTestDictDB(JsonDictDB).test()


def test_jsondictdb_db_create_manual_db():
    with temp_pathname() as dbpath:
        with open(dbpath, "w") as f:
            f.write('{"a": "1", "b": "2", "c":3}')
        d = JsonDictDB(dbpath, autosync=True)
        assert dict(d) == {"a": "1", "b": "2", "c": 3}


def test_jsondictdb_error_not_dict_loaded():
    with temp_pathname() as dbpath:
        with open(dbpath, "w") as f:
            f.write("[]")
        with pytest.raises(TypeError):
            JsonDictDB(dbpath, autosync=True)


# ---------------- TEST ListTxtDatabase --------------- #
def test_txtdictdb_with_helper():
    HelperTestDictDB(TxtDictDB, values=["a", "b", "c"], keys=["1", "2", "3"]).test()


def test_txtdictdb_value_type():
    """Test that the DB only accept txt type"""
    with temp_pathname() as dbpath:
        l = TxtDictDB(dbpath, autosync=False)
        l["a"] = "1"
        l.sync()
        assert "a" in l

        l = TxtDictDB(dbpath, autosync=False)
        assert "a" in l

        with pytest.raises(TypeError):
            l["a"] = 123

        with pytest.raises(TypeError):
            l["a"] = False

        with pytest.raises(TypeError):
            l.update({"b": "1", "a": False})

        # test key
        with pytest.raises(TypeError):
            l[0] = "a"

        with pytest.raises(TypeError):
            l.update({"b": "1", True: "x"})


def test_txtdictdb_no_newline():
    """Test that the DB don't accept newline"""
    with temp_pathname() as dbpath:
        l = TxtDictDB(dbpath, autosync=True)
        l["a"] = "1"
        assert "a" in l

        l = TxtDictDB(dbpath, autosync=True)
        assert "a" in l

        # test value
        with pytest.raises(ValueError):
            l["a"] = "a\nb"

        # test key
        with pytest.raises(ValueError):
            l["a\nb"] = "a"


def test_txtdictdb_sep_not_in_key():
    """Test that the DB don't accept newline"""
    with temp_pathname() as dbpath:
        l = TxtDictDB(dbpath, autosync=True)
        l["a"] = "1"
        assert "a" in l

        l = TxtDictDB(dbpath, autosync=True)
        assert "a" in l

        # test value: Seperator is allowed in value, we only split the first sep
        l["a"] = "a:b"

        # test key
        with pytest.raises(ValueError):
            l["a:b"] = "a"  # not allowed


def test_textdictdb_load_value_with_sep():
    with temp_pathname() as dbpath:
        l = TxtDictDB(dbpath, autosync=True)
        l["a"] = "1:1"
        assert dict(l) == {"a": "1:1"}

        l = TxtDictDB(dbpath, autosync=True)
        assert dict(l) == {"a": "1:1"}


# TODO: test how json files are


def test_txtdictdb_filecontent():
    """Test how the file is inside"""
    with temp_pathname() as dbpath:
        l = TxtDictDB(dbpath, autosync=True)

        l["a"] = "1"
        assert "a" in l
        assert open(dbpath).read() == "a:1\n"

        l = TxtDictDB(dbpath, autosync=True)
        assert open(dbpath).read() == "a:1\n"

        l["b"] = "2"
        assert open(dbpath).read() == "a:1\nb:2\n"

        l.clear()
        assert open(dbpath).read() == ""

        l["a"] = "1"
        l["b"] = "2"
        del l["a"]
        assert open(dbpath).read() == "b:2\n"


def test_txt_db_create_manual_db():
    with temp_pathname() as dbpath:
        with open(dbpath, "w") as f:
            f.write("a:1\n")
        l = TxtDictDB(dbpath, autosync=True)
        assert dict(l) == {"a": "1"}
