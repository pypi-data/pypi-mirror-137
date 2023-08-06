# This file is placed in the Public Domain.


"list of bots"


from .obj import Object


def __dir__():
    return (
        "Fleet",
        "flt"
    )


class Fleet(Object):

    objs = []

    @staticmethod
    def add(o):
        if repr(o) not in [repr(x) for x in Fleet.objs]:
            Fleet.objs.append(o)

    @staticmethod
    def announce(txt):
        for o in Fleet.objs:
            o.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in Fleet.objs:
            if repr(o) == orig:
                return o

    @staticmethod
    def say(orig, channel, txt):
        o = Fleet.byorig(orig)
        if o:
            o.say(channel, txt)
