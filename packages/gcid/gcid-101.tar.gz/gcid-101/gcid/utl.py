# This file is placed in the Public Domain.


"utilities"


def locked(obj):

    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            obj.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                obj.release()
            return res

        lockedfunc.__wrapped__ = func
        return lockedfunc

    return lockeddec
