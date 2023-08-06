import collections
import glob
import inspect
import os
import shutil
import typing
from string import Template
from typing import Any, Callable, Dict, List, Union

import coloring
from koalak.frameworks import home_structure
from koalak.frameworks.home_structure import (
    DirectoryDescription,
    FileDescription,
    normalize_home_structure,
)

from . import databases, exceptions
from .consts import HOMEPATH_NAME, PACKAGE_NAME

"""This module contain the main bases for the project koalak (framework, plugin managers, ...)"""


def __init_subclass__(subcls, **kwargs):

    if "name" not in subcls.__dict__:
        raise ValueError(f"Base plugin must have the attribute 'name'")

    # add the plugin
    name = subcls.__dict__["name"]
    pm = subcls._fwm["plugin_manager"]
    if name in pm._plugins:
        raise exceptions.PluginAlreadyExistException(f"plugin {name} already exist")

    pm._plugins[name] = subcls

    # abstract class
    if FwmConfig.is_abstract(subcls):
        pass


def init_subclass(subcls, **kwargs):
    subcls._pluginmanager._register(subcls)


class FwmConfig:
    """Class responsible to handle internal config in objects
    like plugins. Ex: @abstract"""

    dict_name = PACKAGE_NAME

    @classmethod
    def update(cls, key, value):
        pass

    @classmethod
    def get(cls, key):
        pass

    @classmethod
    def set_abstract(cls, target_cls):
        cls.update("abstract", True)

    @classmethod
    def is_abstract(cls, target_cls):
        pass


class KoalakContainer:
    """Main container for koalak classes (framework, plugin_manager, hooks, ...)
    Act between dict and list, store named item in dict and unamed item in list
    """

    def __init__(self):
        self._dict_data = {}
        self._list_data = []

    def _add_item(self, object, name=None):
        # FIXME: item must be a string?
        if name is None:
            self._list_data.append(object)
        else:
            self._dict_data[name] = object

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._dict_data
        else:
            return item.name in self._dict_data

    def __getitem__(self, item):
        return self._dict_data[item]

    def __iter__(self):
        yield from self._dict_data.values()
        yield from self._list_data

    def __len__(self):
        return len(self._dict_data) + len(self._list_data)


class Plugin:
    pass


def mkpluginmanager(*args, **kwargs):
    return PluginManager(*args, **kwargs)


class ConstraintAttr:
    def __init__(self, name: str = None, type=None, inheritable: bool = True):
        """

        Args:
            name: name of the class attribute
            type: type of the class attribute
            inheritable: if the attribute can be inherited (True)
                or if each class must define the class attribute (False)
        """
        self.name = name
        self.type = type
        self.inheritable = inheritable

    def check(self, plugin):
        if self.name is None:
            raise TypeError("Must set the attribute name")
        if self.inheritable:
            has_attr = hasattr(plugin, self.name)
        else:
            has_attr = self.name in plugin.__dict__

        if not has_attr:
            raise TypeError(
                f"plugin {plugin.__name__!r} must have the class attribute {self.name!r}"
            )

        plugin_attr = getattr(plugin, self.name)
        # Check type
        if self.type is not None:
            if not isinstance(plugin_attr, self.type):
                raise TypeError(
                    f"class attribute {self.name} must be of type {self.type}"
                )


class PluginManager(KoalakContainer):
    """

    How it work:

    """

    def __init__(self, name: str = None, *, homepath=None):
        super().__init__()

        # FIXME: plugin without name?
        self.name: str = name
        self.baseplugin = None
        self.homepath = homepath
        self._plugins = {}
        self._initialized = False
        self._constraints = []

    def __repr__(self):
        if self.name:
            return f"<PluginManager [{self.name}]>"
        else:
            return f"<PluginManager>"

    def __str__(self):
        return self.__repr__()

    def _assert_baseplugin(self):
        if self.baseplugin is None:
            raise TabError("BasePlugin not initiated!")

    def _register(self, plugin):
        if self.baseplugin is None:
            raise TypeError(
                "Can't register plugin without baseplugin. use mkbaseplugin before"
            )

        # Fixme: better think abstract class
        is_abstract = "abstract" in plugin.__dict__
        if not is_abstract:
            # Check constraint before registring
            for contraint in self._constraints:
                contraint.check(plugin)

            self._add_item(plugin, plugin.name)

    def mkbaseplugin(self, baseplugin):
        self.baseplugin = baseplugin
        baseplugin._pluginmanager = self
        baseplugin.__init_subclass__ = classmethod(init_subclass)

        attrs_to_del = []  # we can't del in loop
        for name, constraint in baseplugin.__dict__.items():
            if isinstance(constraint, ConstraintAttr):
                constraint.name = name
                self._constraints.append(constraint)
                attrs_to_del.append(name)
        for attr_name in attrs_to_del:
            delattr(baseplugin, attr_name)

        # All custom plugins (loaded from home) have _is_home_plugin to True
        self.baseplugin._is_home_plugin = False
        return baseplugin

    def init(self, _homepath_initialized: set = None):
        _homepath_initialized = _homepath_initialized or set()
        if self.homepath is None:
            raise TypeError("You can not init a plugin mananger without homepath")

        if self._initialized:
            raise TypeError("Plugin Already initiated")
        self._initialized = True

        if self.homepath in _homepath_initialized:
            return
        self._init_home()
        self._load_plugins()

    def attr(self, type=None, inheritable=True):
        return ConstraintAttr(type=type, inheritable=inheritable)

    def get_home_plugins(self):
        """Get plugins loaded from home/plugins"""
        for e in self:
            if e._is_home_plugin:
                yield e

    def _load_plugins(self):
        """Load home plugins"""
        for python_path in glob.glob(os.path.join(self.homepath, "*.py")):
            with open(python_path) as f:
                data = f.read()
                execution_context = {}
                exec(data, execution_context)
                for object_name, object in execution_context.items():
                    if inspect.isclass(object) and issubclass(object, self.baseplugin):
                        if object is self.baseplugin:
                            continue
                        object._is_home_plugin = True

    def _init_home(self):
        if not self.homepath:
            return
        if not os.path.exists(self.homepath):
            os.makedirs(self.homepath)
        elif os.path.isfile(self.homepath):
            raise NotADirectoryError("Home path is not a directory")
        # else it's a directory already created


class HookManager:
    def __init__(self, name, spec_func):
        self.name = name
        self.spec_func = spec_func
        self._hooks = {}

    def register(self, func):
        func_name = func.__name__
        if func_name in self._hooks:
            raise exceptions.HookAlreadyExistException(
                f"hook {func_name} already exist"
            )

        self._hooks[func_name] = func
        return func

    def get_hook(self, hook_name: str) -> Callable:
        return self._hooks[hook_name]

    def get_hooks(self) -> List[Callable]:
        return list(self._hooks.values())

    def runall(self, *args, **kwargs):
        results = []
        for func in self._hooks.values():
            result = func(*args, **kwargs)
            results.append(result)
        return results


class Printer:
    pass


NOT_ALLOWED_VARIABLE_NAMES = ["home", "userhome"]


class FrameworkVariables(collections.UserDict):
    def __setitem__(self, key, value):
        if key in NOT_ALLOWED_VARIABLE_NAMES:
            raise TypeError(f"Variable name {key!r} is not allowed")
        super().__setitem__(key, value)

    # FIXME: what if key is not a string?
    def set(self, key: str, value: Any, substitute=False) -> None:
        """Same as setitem with the extra parameter substitute
        Args:
            substitute(bool): Substitute value with template if True
        """
        if substitute:
            value = self.substitute_string(value)

        self.__setitem__(key, value)

    def substitute_string(self, string: str):
        return Template(string).substitute(self.data)


class ReadonlyDict(collections.UserDict):
    def __setitem__(self, key, value):
        raise RuntimeError("Cannot modify read only dict")


class FrameworkDatabases(collections.UserDict):
    def __setitem__(self, key, value):
        raise RuntimeError("Cannot modify Databases")


class Framework:
    def __init__(
        self,
        name: str = None,
        *,
        homepath: str = None,
        home_structure=None,
        variables: Dict[str, Any] = None,
        version: str = None,
    ):

        # TODO: add param substitute_vars, to substitute variables on init?
        if variables is None:
            variables = {}

        self.variables = FrameworkVariables(variables)

        self.name: str = name
        self.homepath: str = homepath
        if version is None:
            version = "0.0.0"
        self.version: str = version
        # The framework can be initialized if it has a name or a home path
        self._can_be_initialized = name or homepath
        if self._can_be_initialized and self.homepath is None:
            self.homepath = os.path.expanduser(
                os.path.join("~", f".{HOMEPATH_NAME}", self.name)
            )

        if home_structure is None:
            home_structure = []
        else:
            home_structure = normalize_home_structure(home_structure)
        self._home_structure = home_structure
        # self._plugin_managers: Dict[str, PluginManager] = {}
        self.plugin_managers = KoalakContainer()
        self._hook_managers: Dict[str, HookManager] = {}
        self._initialized: bool = False

        # --- variables ---
        # TODO: test home variable with unnamed framework
        if self.homepath:
            self.variables.data["home"] = self.homepath
        self.variables.data["userhome"] = os.path.expanduser("~")
        self.printer = Printer()

        # --- databases ---
        self.list_db: typing.Mapping[str : databases.ListDB] = FrameworkDatabases()
        self.dict_db: typing.Mapping[str : databases.DictDB] = FrameworkDatabases()

    def __repr__(self):
        if self.name:
            return f"<Framework [{self.name}]>"
        else:
            return f"<Framework>"

    def __str__(self):
        return self.__repr__()

    def fixture(self, function):
        pass

    def init(self):
        # We can init a framework if he has a name or a homepath
        if self._initialized:
            raise TypeError(f"Framework {self.name} already initialized")
        self._initialized = True

        # Check if it can be initialized
        if not self._can_be_initialized:
            raise TypeError(
                f"Framework need a name or a homepath in order to be initialized"
            )

        # Check if it's already initialized (in previous run)
        if not self._is_initialized():
            self._init_home()

        # Init plugins
        homepath_initialized = set()  # Don't initialize twice the same homepath!
        for plugin_manager in self.plugin_managers:
            homepath = plugin_manager.homepath
            plugin_manager.init(_homepath_initialized=homepath_initialized)
            homepath_initialized.add(homepath)

        # TODO: at the end init the framework database (version)

    def _is_initialized(self):
        return os.path.isdir(self.homepath)

    def _init_home(self, parent_path=None, nodes=None):
        """Recursive function"""
        # FIXME: add support for nodes as list of string and dict
        # FIXME: see _normalize_home_node and skipped tests
        # TODO: add support for tree ``tree -Jd``
        # TODO: add this as a standalone function
        if parent_path is None:
            os.makedirs(self.homepath)
            parent_path = self.homepath

        if nodes is None:
            nodes = self._home_structure

        for node in nodes:
            path = os.path.join(parent_path, node.name)
            if isinstance(node, FileDescription):
                # run before_normalize hooks actions
                for action in node.actions:
                    action.before_normalize(node, self)

                norimalized_file = home_structure.normalize_file_description(
                    node, parent_path, self
                )

                # run after_normalize hooks actions
                for action in node.actions:
                    action.after_normalize(norimalized_file)

                with open(norimalized_file.path, "w") as f:
                    f.write(norimalized_file.content)

                # run after_normalize hooks actions
                for action in node.actions:
                    action.after_creation(norimalized_file)

            elif isinstance(node, DirectoryDescription):
                os.mkdir(path)
                self._init_home(path, node.nodes)

    # @defaultargs(firstarg=str)
    def mkhkmanager(self, func, hook_name):
        pass

    def mkhookmanager(self, hook_name_or_func: Union[Callable, str]):
        def _mkhookmanager(spec_function):
            if hook_name in self._hook_managers:
                raise exceptions.HookManagerAlreadyExistException(
                    f"hook {hook_name} already exist in {self.name} framework"
                )

            hm = HookManager(hook_name, spec_function)
            self._hook_managers[hook_name] = hm
            return hm

        if isinstance(hook_name_or_func, str):
            hook_name = hook_name_or_func
        elif inspect.isfunction(hook_name_or_func):
            hook_name = hook_name_or_func.__name__
            return _mkhookmanager(hook_name_or_func)
        else:
            pass
            # TODO: raise not handled type

        return _mkhookmanager

    def mkpluginmanager(self, pluginmanager_name: str = None, homepath=None):

        if homepath is None and self.homepath:
            homepath = os.path.join(self.homepath, "plugins")
        elif homepath and self.homepath:
            homepath = os.path.join(self.homepath, homepath)

        pluginmanager = PluginManager(pluginmanager_name, homepath=homepath)
        self.plugin_managers._add_item(pluginmanager, pluginmanager_name)
        # self._plugin_managers[pluginmanager_name] = pluginmanager
        return pluginmanager

    def mkpluginmanager2(self, plugin_name: str):
        def _mkplugin(base_cls):
            if plugin_name in self._plugin_managers:
                raise exceptions.PluginManagerAlreadyExistException(
                    f"plugin manager {plugin_name} already exist"
                )
            pm = PluginManager(plugin_name, base_cls)
            self._plugin_managers[plugin_name] = pm

            base_cls._fwm = {"plugin_manager": pm}
            base_cls.__init_subclass__ = classmethod(__init_subclass__)
            return base_cls

        return _mkplugin

    def get_plugins(self, plugin_manager_name: str):
        from warnings import warn

        warn("get_plugins is deprecated use plugin_managers instead")

        return self.plugin_managers[plugin_manager_name].get_plugins()

    def get_plugin_manager(self, plugin_manager_name: str) -> PluginManager:
        from warnings import warn

        warn("get_plugin_manager is deprecated use plugin_managers[<name>] instead")
        return self.plugin_managers[plugin_manager_name]

    def get_hook_manager(self, hook_manager_name: str) -> HookManager:
        return self._hook_managers[hook_manager_name]

    def get_hook_managers(self):
        return list(self._hook_managers.values())

    def get_hook(self, hook_manager_name, hook_name):
        return self._hook_managers[hook_manager_name].get_hook(hook_name)

    def get_hooks(self, hook_manager_name):
        return self._hook_managers[hook_manager_name].get_hooks()

    def get_plugin(self, plugin_manager_name: str, plugin_name: str):
        # TODO: keep this function or not?
        return self.plugin_managers[plugin_manager_name].get_plugin(plugin_name)

    def create_list_db(
        self, name, *, path=None, type=None, unique=None
    ) -> databases.ListDB:
        # FIXME: init before or create database? or not important?
        # FIXME: check that db name is correct (no new lines..) as identifier
        if type is None:
            type = "json"
        elif type not in ["txt", "json"]:
            raise ValueError(f"Unknown type of db {type!r}")

        if path is None:
            path = f"$home/databases/list/{name}.{type}"

        path = self.substitute_string(path)
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)  # create DB directory

        if type == "json":
            cls_db = databases.JsonListDB
        elif type == "txt":
            cls_db = databases.TxtListDB
        else:
            # ignore this line in coverage because we check type in the begening of this function
            #  this line is here juste to help us avoid programing errors
            raise ValueError(f"Unknown type of db {type!r}")  # pragma: no cover
        db = cls_db(path, unique=unique)

        self.list_db.data[name] = db
        return db

    def create_dict_db(
        self, name, *, path=None, type=None, unique=None, **kwargs
    ) -> databases.DictDB:
        """
        Args:
            kwargs: kwargs argument to pass to DictDB
        """
        # FIXME: init before or create database? or not important?
        # FIXME: check that db name is correct (no new lines..) as identifier
        if type is None:
            type = "json"
        elif type not in ["txt", "json"]:
            raise ValueError(f"Unknown type of db {type!r}")

        if path is None:
            path = f"$home/databases/dict/{name}.{type}"

        path = self.substitute_string(path)
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)  # create DB directory

        if type == "json":
            cls_db = databases.JsonDictDB
        elif type == "txt":
            cls_db = databases.TxtDictDB
        else:
            # ignore this line in coverage because we check type in the begening of this function
            #  this line is here juste to help us avoid programing errors
            raise ValueError(f"Unknown type of db {type!r}")  # pragma: no cover
        db = cls_db(path, unique=unique, **kwargs)

        self.dict_db.data[name] = db
        return db

    def print_info(self, details=True):
        """Function to debug and see main information about this framewoork"""
        # TODO: coloring add coloring.print_title
        coloring.print_green(f"Framework {self.name}")

        print("Plugin managers:")
        for pm in self.plugin_managers:
            print(f"\t{pm.name} ({len(pm)})")

        print("Hooks:")
        for hook_name, hook in self._hook_managers.items():
            print(f"\t{hook_name} ({len(hook)})")
        print("Variables:")
        for varname, value in self.variables.items():
            print(f"\t{varname}: {value}")

        # databases
        print("Databases:")
        print("\tList DB:")
        for db_name, db in self.list_db.items():
            print(f"\t\t{db_name} ({len(db)}) [{db.uri}]")

        print("\tDict DB:")
        for db_name, db in self.dict_db.items():
            print(f"\t\t{db_name} ({len(db)}) [{db.uri}]")
        # TODO: plugin_managers/hooks
        # TODO: change naming

    def uninstall(self):
        """Undo every thing init did"""
        # TODO: can't be called without init being called
        # TODO: test! test plugins (they might have their own path)
        # Remove the home path
        shutil.rmtree(self.homepath)

        # undo file actions
        # FIXME: must be recursive! implement iternodes
        for node in self._home_structure:
            if isinstance(node, FileDescription):
                for action in node.actions:
                    action.uninstall(node, self)

    # ========= #
    # VARIABLES #
    # ========= #
    def substitute_string(self, string: str):
        return self.variables.substitute_string(string)


class FrameworkManager(KoalakContainer):
    """This class represent in a way the library Koalak"""

    def __init__(self):
        super().__init__()
        self._unique_framework_name_counter = 0

    def mkframework(
        self,
        framework_name: str = None,
        *,
        homepath=None,
        home_structure=None,
        variables=None,
        version: str = None,
    ) -> Framework:
        if framework_name and framework_name in self:
            raise exceptions.FrameworkAlreadyExistException(
                f"Framework {framework_name} already exist"
            )

        framework = Framework(
            framework_name,
            homepath=homepath,
            home_structure=home_structure,
            variables=variables,
            version=version,
        )

        self._add_item(framework, framework_name)
        return framework

    def get_framework(self, framework_name: str) -> Framework:
        import warnings

        warnings.warn(
            "get_framework deprecated use frameworks[<name>] instead",
            DeprecationWarning,
        )
        return self[framework_name]

    def get_frameworks(self) -> List[Framework]:
        import warnings

        warnings.warn(
            "get_frameworks deprecated use frameworks instead", DeprecationWarning
        )
        return list(self)

    def generate_unique_framework_name(self):
        while True:
            self._unique_framework_name_counter += 1
            counter = self._unique_framework_name_counter
            name = f"unique_framework_name_{counter}"
            if name not in self:
                return name

    def get_unique_framework_name(self) -> str:
        import warnings

        warnings.warn(
            "get_unique_framework_name deprecated use generate_unique_framework_name instead",
            DeprecationWarning,
        )
        return self.generate_unique_framework_name()


frameworks = FrameworkManager()
