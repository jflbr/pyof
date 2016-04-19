#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dummy
----------------------------------
Tests for `dummy` module.
"""

import unittest
#from .. import errors
from pyof import errors


class TestPyof(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        assert 1==1

    def test_something_else(self):
        assert 3==3

    def test_relative_import(self):
        assert 3==3



    def tearDown(self):
        pass
