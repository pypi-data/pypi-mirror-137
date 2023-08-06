import koalak
import pytest
from koalak.utils import temp_pathname


# ------ VARIABLES -------
def test_init_variables_in_mkframework():
    framework = koalak.mkframework(variables={"age": 30})
    assert framework.variables["age"] == 30


def test_create_variable():
    framework = koalak.mkframework()
    framework.variables["name"] = "test"
    assert framework.variables["name"] == "test"


def test_update_variable():
    framework = koalak.mkframework(variables={"name": "test"})
    assert framework.variables["name"] == "test"
    framework.variables["name"] = 30
    assert framework.variables["name"] == 30


def test_not_allowed_keyword_variables():
    with pytest.raises(TypeError):
        koalak.mkframework(variables={"home": "path"})

    framework = koalak.mkframework()
    with pytest.raises(TypeError):
        framework.variables["home"] = "test"


def test_substitute_string():
    framework = koalak.mkframework()
    framework.variables["age"] = 25
    assert framework.substitute_string("$age") == "25"
    framework.variables["age"] = 26
    assert framework.substitute_string("my age is $age") == "my age is 26"


def test_default_variables_are_present():
    framework = koalak.mkframework()
    assert "userhome" in framework.variables

    with temp_pathname() as homepath:
        framework = koalak.mkframework(homepath)
        print("variables", framework.variables)
        assert framework.variables["home"] == homepath

    # FIXME: what is the expected behaviour of 'home' variable for unamed framework


def test_remove_variable():
    framework = koalak.mkframework()
    framework.variables["age"] = 25
    assert "age" in framework.variables
    del framework.variables["age"]
    assert "age" not in framework.variables


def test_substitutable_variables():
    with temp_pathname() as homepath:
        framework = koalak.mkframework(homepath)
        framework.variables.set("mypath", "$home/mypath", substitute=True)
        assert framework.variables["mypath"] == f"{homepath}/mypath"

    with temp_pathname() as homepath:
        framework = koalak.mkframework(homepath)
        framework.variables.set("mypath", "$home/mypath", substitute=False)
        assert framework.variables["mypath"] == f"$home/mypath"

    with temp_pathname() as homepath:
        framework = koalak.mkframework(homepath)
        framework.variables.set("mypath", "$home/mypath")
        assert framework.variables["mypath"] == f"$home/mypath"
