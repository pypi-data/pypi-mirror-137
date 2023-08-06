# This file is placed in the Public Domain.


"database"


import datetime
import json
import os
import time
import _thread


from .cls import Cls
from .fnc import cdir, search
from .jsn import ObjectDecoder, ObjectEncoder
from .krn import Cfg
from .obj import Object, update
from .utl import locked


def __dir__():
    return (
         'Db',
         'all',
         'find',
         'load',
         'last',
         'read',
         'save',
         'dump',
    )


dblock = _thread.allocate_lock()


class Db(Object):

    names = Object()

    def all(self, otype, selector=None, index=None, timed=None):
        nr = -1
        if selector is None:
            selector = {}
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

    def deleted(self, otype):
        for fn in fns(otype):
            o = hook(fn)
            if "_deleted" not in o or not o._deleted:
                continue
            yield fn, o

    def every(self, selector=None, index=None, timed=None):
        assert Cfg.wd
        if selector is None:
            selector = {}
        nr = -1
        for otype in os.listdir(os.path.join(Cfg.wd, "store")):
            for fn in fns(otype, timed):
                o = hook(fn)
                if selector and not search(o, selector):
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                nr += 1
                if index is not None and nr != index:
                    continue
                yield fn, o

    def find(self, otype, selector=None, index=None, timed=None):
        if selector is None:
            selector = {}
        got = False
        nr = -1
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            got = True
            yield (fn, o)
        if got:
            return (None, None)
        return None

    def lastmatch(self, otype, selector=None, index=None, timed=None):
        db = Db()
        res = sorted(db.find(otype, selector, index, timed),
                     key=lambda x: fntime(x[0]))
        if res:
            return res[-1]
        return (None, None)

    def lastobject(self, o):
        return self.lasttype(o.__otype__)

    def lasttype(self, otype):
        fnn = fns(otype)
        if fnn:
            return hook(fnn[-1])
        return None

    def lastfn(self, otype):
        fn = fns(otype)
        if fn:
            fnn = fn[-1]
            return (fnn, hook(fnn))
        return (None, None)

    @staticmethod
    def types():
        assert Cfg.wd
        path = os.path.join(Cfg.wd, "store")
        if not os.path.exists(path):
            return []
        return sorted(os.listdir(path))


def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        t += float("." + rest)
    else:
        t = 0
    return t


@locked(dblock)
def fns(name, timed=None):
    if not name:
        return []
    assert Cfg.wd
    p = os.path.join(Cfg.wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(p) < timed["from"]
                    ):
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)


@locked(dblock)
def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    cls = Cls.get(cname)
    if cls:
        o = cls()
    else:
        o = Object()
    fn = os.sep.join(oname)
    load(o, fn)
    return o


def listfiles(workdir):
    path = os.path.join(Cfg.wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def all(timed=None):
    assert Cfg.wd
    p = os.path.join(Cfg.wd, "store")
    for name in os.listdir(p):
        for fn in fns(name):
            yield fn


def dump(o, opath):
    cdir(opath)
    with open(opath, "w") as ofile:
        json.dump(
            o.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return o.__stp__


def find(name, selector=None, index=None, timed=None, names=None):
    db = Db()
    if not names:
        names = Cls.full(name)
    for n in names:
        for fn, o in db.find(n, selector, index, timed):
            yield fn, o


def last(o):
    db = Db()
    path, obj = db.lastfn(o.__otype__)
    if obj:
        update(o, obj)
    if path:
        splitted = path.split(os.sep)
        stp = os.sep.join(splitted[-4:])
        return stp
    return None


def load(o, opath):
    if opath.count(os.sep) != 3:
        return
    assert Cfg.wd
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Cfg.wd, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r") as ofile:
            d = json.load(ofile, cls=ObjectDecoder)
            update(o, d)
    o.__stp__ = stp


def save(o):
    assert Cfg.wd
    prv = os.sep.join(o.__stp__.split(os.sep)[:2])
    o.__stp__ = os.path.join(prv,
                             os.sep.join(str(datetime.datetime.now()).split()))
    opath = os.path.join(Cfg.wd, "store", o.__stp__)
    dump(o, opath)
    os.chmod(opath, 0o444)
    return o.__stp__
