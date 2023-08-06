import abc
import collections
import json
import os
import shutil
import typing
from typing import Any, List

from koalak.utils import get_prefixed_callables_of_object, temp_pathname

"""
Introduction:
=============
These databases are meant for light usage since they are slow/heavy
and they sinc each time
It is designed to be used as a builtin list or dict


Existing similar project (using files):
=======================================
- sqlite
- text/csv/json
- tinydb
- dataset
- pickledb
- shelve (stdlib)
    - https://code.activestate.com/recipes/576642/ => I used a bit of this
- dbm (key/value)
https://docs.python.org/3/library/persistence.html


Known problems/ To know:
=======================
- Some DB cannot support all types
    - txt: only strings without newlines
    - json: no object
    - ...
- Writeback? (if we use shelve => for the moment not used)
- Autosync
- Attomic sync?


Available databases (implemented or to implement):
==================================================
- list (txt/json/yaml/pickle)
- dict (txt with separator, json, yaml, pickle)
- table? (csv, json, yaml, pickle)
"""

# TODO add Pickle/Yaml on list DB and dict DB
# TODO: Think about delayed opening DB in framework?


class Database(abc.ABC):
    def __init__(self, uri: str, *, mode: str = None, autosync: bool = None):
        """
        Args:
            uri(str): The uri (path) of the DB
            mode(str):
            autosync(bool): if True write to disk after each modification
        """
        if autosync is None:
            autosync = True

        self.uri = uri
        self.autosync = autosync
        self.mode = mode
        self._nb_sync = 0  # TODO: implement me

    def sync(self):
        """Write to disk"""
        if self._synced:
            return
        with temp_pathname() as tmp_dbfile:
            self.dump(tmp_dbfile)

            shutil.move(tmp_dbfile, self.uri)  # atomic commit
            if self.mode is not None:
                os.chmod(self.filename, self.mode)
        self._synced = True
        self._nb_sync += 1

    def _not_synced(self):
        """Set sync at false and autosync"""
        self._synced = False
        if self.autosync:
            self.sync()

    def _check_value(self, e):
        """This method should be implemented on class that have constraint on values"""
        pass

    @abc.abstractmethod
    def dump(self, filepath):
        pass  # pragma: no cover

    @abc.abstractmethod
    def load(self, filepath) -> list:
        pass  # pragma: no cover


class DictDB(collections.UserDict, Database):
    # TODO: add other functions? like count, index ...
    @abc.abstractmethod
    def __init__(self, uri, initdict=None, *, autosync=None, unique=None):
        """Subclass must call super().__init__ and sync()
        We can not call sync on this class because some subclass might need
            extra attributes to call sync() (wich calles dump())

        Notes:
            unique are heavy, at each insertion we will check all values"""
        # TODO: Optimize unique with an inversed dict?

        Database.__init__(self, uri, autosync=autosync)
        # We can not call UserDict.__init__ because it will call self.update()
        #   => self.__setitem__ => self._autosync() => self.sync() => self.dump()

        if unique is None:
            unique = False

        if os.path.exists(uri) and initdict is not None:
            raise TypeError(
                f"DB already created, it can't be initiated with existing dict"
            )

        # We can not call UserDict.__init__ because it will call self.update()
        #   => self.__setitem__ => self._autosync() => self.sync() => self.dump()
        if initdict is None:
            initdict = {}
        self.data = initdict

        self.unique = unique
        self._synced = False  # To optimize useless sync()

        if os.path.exists(uri):
            self.data = self.load(uri)

    def _check_unique(self, key, value):
        if self.unique:
            if self[key] == value:
                return
            for k, v in self.items():
                if v == value:
                    raise ValueError(f"Key")

    def __setitem__(self, key, value):
        # TODO: check value/ check unique
        self._check_value((key, value))
        self.data.__setitem__(key, value)
        self._not_synced()

    def update(self, other):
        # TODO: implement unique
        for k, v in other.items():
            self._check_value((k, v))
            self.data[k] = v
        self._not_synced()

    def __delitem__(self, key):
        self.data.__delitem__(key)
        self._not_synced()

    # TODO: copy


class ListDB(collections.UserList, Database):
    """Abstract class for list database"""

    # 4 Types: Txt, Json, Yaml, Pickle
    # TODO: add constraint feature?
    # TODO: test when the file db exist and an object is present
    # TODO: create generic class WrapperList, wich act like UserList
    #   but will always return a normal list instead of __class__
    #   it will be used for when we always wantto return a normal list like now
    @abc.abstractmethod
    def __init__(self, uri, initlist=None, *, autosync=None, unique=None):
        """Subclass must call super().__init__ and sync()
        We can not call sync on this class because some subclass might need
            extra attributes to call sync() (wich calles dump())"""
        Database.__init__(self, uri, autosync=autosync)
        collections.UserList.__init__(self, initlist)
        if unique is None:
            unique = False

        if os.path.exists(uri) and initlist is not None:
            raise TypeError(
                f"DB already created, it can't be initiated with existing list"
            )

        if initlist is None:
            initlist = []

        self.unique = unique
        self._synced = False  # To optimize useless sync()

        if os.path.exists(uri):
            self.data[:] = self.load(uri)

    def _check_unique(self, e, values=None):
        if values is None:
            values = self.data

        if self.unique:
            if not callable(self.unique):
                if e in values:
                    raise ValueError(
                        f"Unique constraint is present, element already present"
                    )
            else:
                # unique is callable
                unique_e = self.unique(e)
                for e in values:
                    if unique_e == self.unique(e):
                        raise ValueError(
                            f"Unique constraint as function is present, element already present"
                        )

    # FIXME: check __iter__ and __str__

    def __getitem__(self, index):
        # Get item will return a normal list and not DBList!
        return self.data.__getitem__(index)

    def __delitem__(self, key):
        self.data.__delitem__(key)
        self._not_synced()

    def __add__(self, other):
        return self.data + list(other)

    def __radd__(self, other):
        return list(other) + self.data

    def __mul__(self, n):
        return self.data * n

    def __rmul__(self, other):
        return self.__mul__(other)

    # FIXME: __copy__
    def __setitem__(self, index, value):
        # FIXME: try to optimize setitem for the concerned index/check_value/check_unique
        self._check_value(value)

        #  must check other items that the indexed one
        if self.unique:
            all_values_but_current_index = self[:index] + self[index + 1 :]
            self._check_unique(value, values=all_values_but_current_index)

        self.data.__setitem__(index, value)
        self._not_synced()

    def append(self, e: Any):
        self._check_unique(e)
        self._check_value(e)

        self.data.append(e)
        self._not_synced()

    def insert(self, index, value):
        self._check_unique(value)
        self._check_value(value)

        self.data.insert(index, value)
        self._not_synced()

    def pop(self, i=-1):
        return_value = self.data.pop(i)
        self._not_synced()
        return return_value

    def remove(self, value: Any):
        self.data.remove(value)
        self._not_synced()

    def clear(self):
        self.data.clear()
        self._not_synced()

    # TODO: def copy(self)

    def reverse(self):
        self.data.reverse()
        self._not_synced()

    def sort(self, *, key=None, reverse=False):
        self.data.sort(key=key, reverse=reverse)
        self._not_synced()

    def extend(self, iterable):
        for e in iterable:
            self._check_unique(e)
            self._check_value(e)
            self.data.append(e)

        self._not_synced()


class JsonDictDB(DictDB):
    # TODO: add update optimized (like extend)
    def __init__(self, uri, obj=None, *, autosync=None, unique=None, indent=4):
        super().__init__(uri, obj, autosync=autosync, unique=unique)

        self.indent = indent
        self.sync()

    def dump(self, filepath):
        with open(filepath, "w") as fileobj:
            json.dump(self.data, fileobj, indent=self.indent)

    def load(self, filepath) -> list:
        with open(filepath) as fileobj:
            l = json.load(fileobj)
            if not isinstance(l, dict):
                raise TypeError(f"Loaded DB is not a dict but {type(l)}")
            return l


class JsonListDB(ListDB):
    def __init__(self, uri, obj=None, *, autosync=None, unique=None, indent=4):
        super().__init__(uri, obj, autosync=autosync, unique=unique)

        self.indent = indent
        self.sync()

    def dump(self, filepath):
        with open(filepath, "w") as fileobj:
            json.dump(self.data, fileobj, indent=self.indent)

    def load(self, filepath) -> list:
        with open(filepath) as fileobj:
            l = json.load(fileobj)
            if not isinstance(l, list):
                raise TypeError(f"Loaded DB is not a list but {type(l)}")
            return l


class TxtListDB(ListDB):
    def __init__(self, uri, initlist=None, *, autosync=None, unique=None):
        super().__init__(uri, initlist, autosync=autosync, unique=unique)
        self.sync()

    def _check_value(self, e):
        if not isinstance(e, str):
            raise TypeError(f"Added element must be of type str and not {type(e)!r}")
        if "\n" in e:
            raise ValueError(f"Added element must not contain newline")

    # TODO: we can optimize this class append can just write
    #   but it is not that simple with autosync ... see removed code

    def dump(self, filepath):
        with open(filepath, "w") as fileobj:
            for e in self.data:
                fileobj.write(e)
                fileobj.write("\n")

    def load(self, filepath) -> list:
        with open(filepath) as fileobj:
            l = fileobj.read().splitlines()
            return l


class TxtDictDB(DictDB):
    def __init__(self, uri, initlist=None, *, sep=":", autosync=None, unique=None):
        self.sep = sep
        super().__init__(uri, initlist, autosync=autosync, unique=unique)
        self.sync()

    def _check_value(self, e):
        k, v = e
        if not isinstance(v, str):
            raise TypeError(f"Added value must be of type str and not {type(v)!r}")
        if "\n" in v:
            raise ValueError(f"Added value must not contain newline")
        if not isinstance(k, str):
            raise TypeError(f"Added key must be of type str and not {type(k)!r}")
        if "\n" in k:
            raise ValueError(f"Added key must not contain newline")
        if self.sep in k:
            raise ValueError(f"Key can't contain the seprator {self.sep!r}")

    # TODO: we can optimize this class append can just write
    #   but it is not that simple with autosync ... see removed code

    def dump(self, filepath):
        with open(filepath, "w") as fileobj:
            for k, v in self.data.items():
                fileobj.write(k)
                fileobj.write(self.sep)
                fileobj.write(v)
                fileobj.write("\n")

    def load(self, filepath) -> list:
        d = {}
        # TODO: what if a key exist twice?
        with open(filepath) as fileobj:
            for line in fileobj:
                k, v = line[:-1].split(self.sep, 1)
                d[k] = v

        return d


# TODO: test dict unique
