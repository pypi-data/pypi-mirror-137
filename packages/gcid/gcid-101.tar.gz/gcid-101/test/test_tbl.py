# This file is placed in the Public Domain.


"table"


import inspect
import os
import sys
import unittest


from gcid.obj import Object, keys, values
from gcid.tbl import Tbl


import gcid.obj


Tbl.add(gcid.obj)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("gcid.obj" in keys(Tbl.mod))
