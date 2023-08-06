# This file is placed in the Public Domain.


"log text"


def __dir__():
    return (
        "log",
    )


from .cls import Cls
from .cmd import Cmd
from .dbs import save
from .obj import Object


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def log(event):
    if not event.rest:
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.rest
    save(o)
    event.reply("ok")


Cls.add(Log)
Cmd.add(log)
