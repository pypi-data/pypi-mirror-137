import os

import koalak
import pytest
from koalak.utils import temp_pathname


def test_simple():
    """Test framework can be created"""
    koalak.mkframework()


def test_double_init():
    """If we call init twice raise Error"""
    with temp_pathname() as pathname:
        framework = koalak.mkframework(homepath=pathname)
        framework.init()
        with pytest.raises(TypeError):
            framework.init()


def test_homepath_is_created():
    """Homepath is created after init"""
    with temp_pathname() as pathname:
        framework = koalak.mkframework(homepath=pathname)
        assert not os.path.exists(pathname)
        framework.init()
        assert os.path.isdir(pathname)


def test__repr__and__str__():
    framework = koalak.mkframework()
    assert repr(framework) == str(framework) == "<Framework>"

    framework = koalak.mkframework("wordlistools")
    assert repr(framework) == str(framework) == "<Framework [wordlistools]>"


# TODO: add constraint on the name of the framework (no new line...)
# TODO: add description of the framework and plugins
# TODO: many pluginsmanagers without name?
# TODO: 2 pluginsmanagers sharing the same folder?
# TODO: When loading a new plugin from home can we sandbox it?
#   to load only this plugin and not an other? or malicious code?
# TODO: add a way te remove a framwork? (from the list to free the memory)


def test_homepath_plugins_alone():
    """Test that folder plugins is created"""
    with temp_pathname() as pathname:
        framework = koalak.mkframework(homepath=pathname)
        framework.mkpluginmanager()
        assert not os.path.exists(pathname)
        framework.init()
        assert os.path.isdir(pathname)
        assert os.path.isdir(os.path.join(pathname, "plugins"))


def test_homepath_plugins_with_homepath():
    """Test that we can chose the folder name of plugins"""
    with temp_pathname() as pathname:
        framework = koalak.mkframework(homepath=pathname)
        plugins = framework.mkpluginmanager(homepath="tools")
        assert not os.path.exists(pathname)
        framework.init()
        assert os.path.isdir(pathname)
        assert not os.path.isdir(os.path.join(pathname, "plugins"))
        assert os.path.isdir(os.path.join(pathname, "tools"))


def test_unique_framework_name():
    """Unique name are correctly generated"""
    for _ in range(10):
        name = koalak.generate_unique_framework_name()
        framework = koalak.mkframework(name)
        assert koalak.frameworks[name] is framework
