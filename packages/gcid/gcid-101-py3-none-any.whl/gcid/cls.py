# This file is placed in the Public Domain.


"classes"


from .fnc import register
from .obj import Object, get


def __dir__():
    return (
        "Cls",
    )


class Cls(Object):

    cls = Object()

    @staticmethod
    def add(clz):
        register(Cls.cls, "%s.%s" % (clz.__module__, clz.__name__), clz)

    @staticmethod
    def full(name):
        name = name.lower()
        res = []
        for cln in Cls.cls:
            if cln.split(".")[-1].lower() == name:
                res.append(cln)
        return res

    @staticmethod
    def get(nm):
        return get(Cls.cls, nm)
