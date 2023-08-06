# This file is placed in the Public Domain.


"functions"


import os
import pathlib


from .obj import Object, items, keys


def __dir__():
    return (
        "cdir",
        "diff",
        "edit",
        "format",
        "register",
        "search",
        "spl"
    )


def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def diff(o1, o2):
    d = Object()
    for k in keys(o2):
        if k in keys(o1) and o1[k] != o2[k]:
            d[k] = o2[k]
    return d


def edit(o, setter):
    for key, v in items(setter):
        register(o, key, v)


def format(o, args="", skip="", sep=" ", **kwargs):
    res = []
    if args:
        ks = spl(args)
    else:
        ks = keys(o)
    for k in ks:
        if k in spl(skip) or k.startswith("_"):
            continue
        v = getattr(o, k, None)
        if isinstance(v, str) and len(v.split()) >= 2:
            txt = '%s="%s"' % (k, v)
        else:
            txt='%s=%s' % (k, v)
        res.append(txt)
    return sep.join(res)


def register(o, k, v):
    setattr(o, k, v)


def search(o, s):
    ok = False
    for k, v in items(s):
        vv = getattr(o, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok


def spl(txt):
    return [x for x in txt.split(",") if x]
