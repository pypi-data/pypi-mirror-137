# This file is placed in the Public Domain.


"table"


from .obj import Object, get


def __dir__():
    return (
        "Tbl",
    )


class Tbl(Object):

    mod = Object()

    @staticmethod
    def add(o):
        Tbl.mod[o.__name__] = o

    @staticmethod
    def get(nm):
        return get(Tbl.mod, nm, None)
