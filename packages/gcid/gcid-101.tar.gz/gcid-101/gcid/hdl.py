# This file is placed in the Public Domain.


"event handler"


import threading


from .cmd import Cmd
from .cbs import Cbs
from .flt import Fleet
from .obj import Object
from .thr import launch


def __dir__():
    return (
        "Handler",
        "dispatch",
    )


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.errors = []
        self.stopped = threading.Event()
        self.register("event", dispatch)

    def announce(self, txt):
        self.raw(txt)

    def handle(self, e):
        e.thrs.append(launch(Cbs.callback, e, name=e.txt))

    def loop(self):
        while not self.stopped.isSet():
            self.handle(self.poll())

    def raw(self, txt):
        raise NotImplementedError

    def register(self, typ, cb):
        Cbs.add(typ, cb)


    def restart(self):
        self.stop()
        self.start()

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        Fleet.add(self)
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        pass


def dispatch(e):
    e.parse()
    f = Cmd.get(e.cmd)
    if f:
        f(e)
        e.show()
    e.ready()
