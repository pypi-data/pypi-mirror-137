# This file is placed in the Public Domain.


"parse"


from .obj import Object, update


def __dir__():
    return (
        "elapsed",
        "parse",
        "spl"
    )


class Token(Object):

    pass


class Word(Token):

    def __init__(self, txt=None):
        super().__init__()
        if txt is None:
            txt = ""
        self.txt = txt


class Option(Token):

    def __init__(self, txt):
        super().__init__()
        if txt.startswith("--"):
            self.opt = txt[2:]
        elif txt.startswith("-"):
            self.opt = txt[1:]


class Getter(Token):

    def __init__(self, txt):
        super().__init__()
        if "==" in txt:
            pre, post = txt.split("==", 1)
        else:
            pre = post = ""
        if pre:
            self[pre] = post


class Setter(Token):

    def __init__(self, txt):
        super().__init__()
        if "=" in txt:
            pre, post = txt.split("=", 1)
        else:
            pre = post = ""
        if pre:
            self[pre] = post


class Skip(Token):

    def __init__(self, txt):
        super().__init__()
        pre = ""
        if txt.endswith("-"):
            if "=" in txt:
                pre, _post = txt.split("=", 1)
            elif "==" in txt:
                pre, _post = txt.split("==", 1)
            else:
                pre = txt
        if pre:
            self[pre] = True


class Url(Token):

    def __init__(self, txt):
        super().__init__()
        self.url = ""
        if txt.startswith("http"):
            self.url = txt


def parse(o, ptxt):
    o.txt = ptxt
    o.otxt = ptxt
    o.gets = Object()
    o.opts = Object()
    o.sets = Object()
    o.skip = Object()
    o.timed = []
    o.index = 0
    args = []
    for t in [Word(txt) for txt in ptxt.rsplit()]:
        u = Url(t.txt)
        if u and "url" in u and u.url:
            args.append(u.url)
            t.txt = t.txt.replace(u.url, "")
        s = Skip(t.txt)
        if s:
            update(o.skip, s)
            t.txt = t.txt[:-1]
        g = Getter(t.txt)
        if g:
            update(o.gets, g)
            continue
        s = Setter(t.txt)
        if s:
            update(o.sets, s)
            continue
        opt = Option(t.txt)
        if opt:
            try:
                o.index = int(opt.opt)
                continue
            except ValueError:
                pass
            if len(opt.opt) > 1:
                for op in opt.opt:
                    o.opts[op] = True
            else:
                o.opts[opt.opt] = True
            continue
        args.append(t.txt)
    if not args:
        o.args = []
        o.cmd = ""
        o.rest = ""
        o.txt = ""
        return o
    o.cmd = args[0]
    o.args = args[1:]
    o.txt = " ".join(args)
    o.rest = " ".join(args[1:])


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def spl(txt):
    return [x for x in txt.split(",") if x]
