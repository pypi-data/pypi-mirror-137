# This file is placed in the Public Domain.


"json"


import json


from .obj import Object, update


def __dir__():
    return (
        'ObjectDecoder',
        'ObjectEncoder',
        "dump",
        "dumps",
        "load",
        "loads"
    )


class ObjectDecoder(json.JSONDecoder):

    def decode(self, s, _w=None):
        v = json.loads(s)
        o = Object()
        update(o, v)
        return o


class ObjectEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


def dump(o, f):
    return json.dump(o, f, cls=ObjectEncoder)


def dumps(o):
    return json.dumps(o, cls=ObjectEncoder)


def load(s, f):
    return json.load(s, f, cls=ObjectDecoder)


def loads(s):
    return json.loads(s, cls=ObjectDecoder)
