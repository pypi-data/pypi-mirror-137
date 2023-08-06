# This file is placed in the Public Domain.


"find objects"


import time


from .cmd import Cmd
from .dbs import Db, find, fntime
from .fnc import format
from .prs import elapsed


def __dir__():
    return (
        "fnd",
    )


def fnd(event):
    if not event.args:
        db = Db()
        res = ",".join(
            sorted({x.split(".")[-1].lower() for x in db.types()}))
        if res:
            event.reply(res)
        return
    otype = event.args[0]
    nr = -1
    got = False
    for fn, o in find(otype):
        nr += 1
        txt = "%s %s" % (str(nr), format(o))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")


Cmd.add(fnd)
