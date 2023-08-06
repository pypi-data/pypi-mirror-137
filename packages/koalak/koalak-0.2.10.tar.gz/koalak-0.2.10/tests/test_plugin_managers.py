import os
import sys
import tempfile

import koalak
import pytest
from koalak.utils import temp_pathname, tmp_module


def test_api_working():
    koalak.mkpluginmanager()
    koalak.mkpluginmanager("something")


def test_unnamed_without_framework():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        pass

    class SimplePlugin(BasePlugin):
        name = "simple"

    assert plugins["simple"] == SimplePlugin
    assert "simple" in plugins
    assert SimplePlugin in plugins
    assert list(plugins) == [SimplePlugin]
    assert len(plugins) == 1


def test_simple_without_framework():
    plugins = koalak.mkpluginmanager("plugin")

    @plugins.mkbaseplugin
    class BasePlugin:
        pass

    class SimplePlugin(BasePlugin):
        name = "simple"

    assert plugins["simple"] == SimplePlugin
    assert "simple" in plugins
    assert SimplePlugin in plugins
    assert list(plugins) == [SimplePlugin]


def test_two_plugins_without_framework():
    plugins = koalak.mkpluginmanager("plugin")

    @plugins.mkbaseplugin
    class BasePlugin:
        pass

    class OnePlugin(BasePlugin):
        name = "one"

    class TwoPlugin(BasePlugin):
        name = "two"

    assert plugins["one"] == OnePlugin
    assert "one" in plugins
    assert OnePlugin in plugins

    assert plugins["two"] == TwoPlugin
    assert "two" in plugins
    assert TwoPlugin in plugins

    assert list(plugins) == [OnePlugin, TwoPlugin]
    assert len(plugins) == 2


def test_with_framework():
    framework = koalak.mkframework()
    plugins = framework.mkpluginmanager("tools")

    @plugins.mkbaseplugin
    class BasePlugin:
        pass

    class SimplePlugin(BasePlugin):
        name = "simple"

    assert plugins["simple"] == SimplePlugin
    assert "simple" in plugins
    assert SimplePlugin in plugins

    assert list(plugins) == [SimplePlugin]
    assert len(plugins) == 1
    assert framework.plugin_managers["tools"] is plugins
    assert len(framework.plugin_managers) == 1


@pytest.mark.skip
def test_error_abstract_method():
    framework = koalak.mkframework()

    @framework.mkpluginmanager("test")
    class BaseTest:
        @framework.abstract
        def x(self):
            pass

    class XTest(BaseTest):
        name = "x"

        def x(self):
            pass

    with pytest.raises(TypeError):

        class YTest(BaseTest):
            name = "y"


def test_abstract_subplugin():
    framework = koalak.mkframework()
    plugins = framework.mkpluginmanager("tools")

    @plugins.mkbaseplugin
    class BasePlugin:
        # This plugin requires the description attribute
        description = plugins.attr(type=str)

    # Plugin A must have the attribute "name"
    with pytest.raises(TypeError):

        class APlugin(BasePlugin):
            name = "A"

    # Abstract class are not checked!
    class AbstractPlugin(BasePlugin):
        abstract = True
        description = "Hey"

    # don't need description since abstract class have it
    class BPlugin(AbstractPlugin):
        name = "B"


def test_load_plugins():
    # TODO: check if this test is correct
    # TODO: Test with existing directory and without
    with tempfile.TemporaryDirectory() as plugin_path:
        plugins = koalak.mkpluginmanager(homepath=plugin_path)

        @plugins.mkbaseplugin
        class BasePlugin:
            pass

        class APlugin:
            name = "A"

        # Temporally create a module so it can be importable by the plugin
        with tmp_module(context={"BasePlugin": BasePlugin}) as module:
            name_module = module.__name__
            # print(name_module, name_module in sys.modules)
            data_file = f"""from {name_module} import BasePlugin
class BPlugin(BasePlugin):
    name = 'B'
    """
            with open(os.path.join(plugin_path, "plugin.py"), "w") as f:
                print("in path", os.path.join(plugin_path, "plugin.py"))
                print("data_file", data_file)
                f.write(data_file)

            # Init folder and plugins
            plugins.init()
            assert plugins["B"].name == "B"  # Just check that "B" is loaded in plugnis


def test_init_without_homepath():
    """We can not initiate a plugin manager without homepath"""
    plugins = koalak.mkpluginmanager()
    with pytest.raises(TypeError):
        plugins.init()  # No error should be raised


def test_double_init():
    """We can init twice"""
    with temp_pathname() as pathname:
        plugins = koalak.mkpluginmanager(homepath=pathname)
        plugins.init()
        with pytest.raises(TypeError):
            plugins.init()


def test_init_with_homepath():
    """Homepath is correctly created"""
    with temp_pathname() as pathname:
        plugins = koalak.mkpluginmanager(homepath=pathname)
        plugins.init()
        assert os.path.isdir(plugins.homepath)


def test_constraint_attribute():
    """Test that attribute "help" is required"""
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        help = plugins.attr()  # help attribute is required

    class APlugin(BasePlugin):
        name = "A"
        help = "Something"

    class BPlugin(BasePlugin):
        name = "A"
        help = 12  # can be of any type

    with pytest.raises(TypeError):
        # Must define help
        class CPlugin(BasePlugin):
            name = "B"


def test_constraint_attr_type():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        help = plugins.attr(type=str)

    class APlugin(BasePlugin):
        name = "A"
        help = "Something"

    with pytest.raises(TypeError):
        # Help must be a string
        class BPlugin(BasePlugin):
            name = "B"
            help = 5


def test_constraint_attr_inheritable_true():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        x = plugins.attr()  # By default inheritable is True

    class APlugin(BasePlugin):
        name = "A"
        x = 1

    class BPlugin(APlugin):
        name = "B"


def test_constraint_attr_inheritable_false():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        x = plugins.attr(inheritable=False)

    class APlugin(BasePlugin):
        name = "A"
        x = 1

    with pytest.raises(TypeError):

        class BPlugin(APlugin):
            name = "B"


def test__repr__and__str__():
    pm = koalak.mkpluginmanager()
    assert repr(pm) == str(pm) == "<PluginManager>"

    pm = koalak.mkpluginmanager("tools")
    assert repr(pm) == str(pm) == "<PluginManager [tools]>"
