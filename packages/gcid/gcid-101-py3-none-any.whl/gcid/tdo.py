# This file is placed in the Public Domain.


"things todo"


def __dir__():
    return (
        "tdo",
    )


import time


from .cls import Cls
from .cmd import Cmd
from .dbs import find, fntime, save
from .obj import Object
from .prs import elapsed
from .thr import starttime


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def tdo(event):
    if not event.rest:
        nr = 0
        for fn, o in find("todo"):
            event.reply("%s %s %s" % (nr, o.txt, elapsed(time.time() - fntime(fn))))
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")


def upt(event):
    event.reply(elapsed(time.time() - starttime))


Cls.add(Todo)
Cmd.add(tdo)
