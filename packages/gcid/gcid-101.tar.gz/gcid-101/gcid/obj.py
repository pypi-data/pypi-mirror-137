# This file is placed in the Public Domain.


"object"


import copy as copying
import datetime
import os
import uuid


def __dir__():
    return (
        'Object',
        'clear',
        'copy',
        'fromkeys',
        'get',
        'items',
        'keys',
        'pop',
        'popitem',
        'setdefault',
        'update',
        'values'
    )


class Object:

    __slots__ = (
        "__dict__",
        "__otype__",
        "__stp__",
    )

    def __init__(self):
        object.__init__(self)
        self.__otype__ = str(type(self)).split()[-1][1:-2]
        self.__stp__ = os.path.join(
            self.__otype__,
            str(uuid.uuid4()),
            os.sep.join(str(datetime.datetime.now()).split()),
        )

    def __class_getitem__(cls):
        return cls.__dict__.__class_geitem__(cls)

    def __contains__(self, k):
        if k in self.__dict__.keys():
            return True
        return False

    def __delitem__(self, k):
        if k in self:
            del self.__dict__[k]

    def __dir__(self):
        return (
            '__class__',
            '__class_getitem__',
            '__contains__',
            '__delattr__',
            '__delitem__',
            '__dir__',
            '__doc__',
            '__eq__',
            '__format__',
            '__ge__',
            '__getattribute__',
            '__getitem__',
            '__gt__',
            '__hash__',
            '__init__',
            '__init_subclass__',
            '__ior__',
            '__iter__',
            '__le__',
            '__len__',
            '__lt__',
            '__ne__',
            '__new__',
            '__or__',
            '__reduce__',
            '__reduce_ex__',
            '__repr__',
            '__reversed__',
            '__ror__',
            '__setattr__',
            '__setitem__',
            '__sizeof__',
            '__str__',
            '__subclasshook__'
        )

    def __eq__(self, o):
        return len(self.__dict__) == len(o.__dict__)

    def __getitem__(self, k):
        return self.__dict__[k]

    def __ior__(self, o):
        return self.__dict__.__ior__(o)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __le__(self, o):
        return len(self) <= len(o)

    def __lt__(self, o):
        return len(self) < len(o)

    def __ge__(self, o):
        return len(self) >= len(o)

    def __gt__(self, o):
        return len(self) > len(o)

    def __hash__(self):
        return id(self)

    def __ne__(self, o):
        return len(self.__dict__) != len(o.__dict__)

    def __reduce__(self):
        pass

    def __reduce_ex__(self, k):
        pass

    def __reversed__(self):
        return self.__dict__.__reversed__()

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __oqn__(self):
        return "<%s.%s object at %s>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
        )

    def __ror__(self, o):
        return self.__dict__.__ror__(o)

    def __str__(self):
        return str(self.__dict__)


def clear(o):
    o.__dict__ = {}


def copy(o):
    return copying.copy(o)


def fromkeys(iterable, value=None):
    o = Object()
    for i in iterable:
        o[i] = value
    return o


def get(o, key, default=None):
    return o.__dict__.get(key, default)


def items(o):
    try:
        return o.__dict__.items()
    except AttributeError:
        return o.items()


def keys(o):
    try:
        return o.__dict__.keys()
    except TypeError:
        return o.keys()


def pop(o, k, d=None):
    try:
        return o[k]
    except KeyError as ex:
        if d:
            return d
        raise KeyError from ex


def popitem(o):
    k = keys(o)
    if k:
        v = o[k]
        del o[k]
        return (k, v)
    raise KeyError


def setdefault(o, key, default=None):
    if key not in o:
        o[key] = default
    return o[key]


def update(o, data):
    try:
        o.__dict__.update(vars(data))
    except TypeError:
        o.__dict__.update(data)
    return o


def values(o):
    try:
        return o.__dict__.values()
    except TypeError:
        return o.values()
