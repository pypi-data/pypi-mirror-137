"""This module test DB interaction with framework, the DB is tested in the file test_databases"""
import koalak
import pytest
from koalak.databases import JsonListDB, TxtListDB
from koalak.utils import temp_pathname


# TODO: test db without
def test_list_db():
    with temp_pathname() as homepath:
        framework = koalak.mkframework(homepath)
        assert len(framework.list_db) == 0

        txt_db = framework.create_list_db("txt_db", type="txt")

        assert isinstance(txt_db, TxtListDB)
        assert framework.list_db["txt_db"] is txt_db
        assert "txt_db" in framework.list_db
        assert len(framework.list_db) == 1
        assert txt_db.uri == f"{homepath}/databases/list/txt_db.txt"

        json_db = framework.create_list_db("json_db", type="json")
        assert isinstance(json_db, JsonListDB)
        assert framework.list_db["json_db"] is json_db
        assert "json_db" in framework.list_db
        assert len(framework.list_db) == 2
        assert json_db.uri == f"{homepath}/databases/list/json_db.json"


def test_list_db_with_path():
    with temp_pathname() as homepath, temp_pathname() as dbpath, temp_pathname() as dbpath2:
        framework = koalak.mkframework(homepath)
        assert len(framework.list_db) == 0

        txt_db = framework.create_list_db("txt_db", path=dbpath, type="txt")

        assert isinstance(txt_db, TxtListDB)
        assert framework.list_db["txt_db"] is txt_db
        assert "txt_db" in framework.list_db
        assert len(framework.list_db) == 1
        assert txt_db.uri == dbpath

        json_db = framework.create_list_db("json_db", path=dbpath2, type="json")
        assert isinstance(json_db, JsonListDB)
        assert framework.list_db["json_db"] is json_db
        assert "json_db" in framework.list_db
        assert len(framework.list_db) == 2
        assert json_db.uri == dbpath2


# TODO: test unamed framework with DB
def test_list_db_errors():
    # Test modifying list_db directly
    with temp_pathname() as homepath, temp_pathname() as dbpath:
        framework = koalak.mkframework(homepath)
        with pytest.raises(RuntimeError):
            framework.list_db["mydb"] = TxtListDB(dbpath)

    # test wrong type
    with temp_pathname() as homepath:
        framework = koalak.mkframework(homepath)
        with pytest.raises(ValueError):
            db = framework.create_list_db("db", type="wrongtype")


def test_default_db_type():
    """Default db is json"""
    with temp_pathname() as homepath:
        framework = koalak.mkframework(homepath)
        db = framework.create_list_db("db")
        assert isinstance(db, JsonListDB)
