# This file is placed in the Public Domain.


"repeater"


from .tmr import Timer
from .thr import launch


def __dir__():
    return (
        "Repeater",
    )


class Repeater(Timer):

    def run(self):
        thr = launch(self.start)
        super().run()
        return thr
