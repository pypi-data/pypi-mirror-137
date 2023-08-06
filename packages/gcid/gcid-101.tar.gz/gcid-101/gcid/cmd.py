# This file is placed in the Public Domain


"command"


from .obj import Object, get, keys
from .fnc import register


def __dir__():
    return (
        "cmd",
    )

class Cmd(Object):

    cmd = Object()

    @staticmethod
    def add(command):
        register(Cmd.cmd, command.__name__, command)

    @staticmethod
    def get(command):
        f =  get(Cmd.cmd, command)
        return f


def cmd(event):
    event.reply(",".join((sorted(keys(Cmd.cmd)))))


Cmd.add(cmd)
