#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_decorators
----------------------------------
Tests for `decorators` module.
"""

import unittest
from pyof import config
from pyof import decorators




# @decorators.as_service(name="AService",config_path="App.Services.Mine")
# class AService(object):
#   """docstring for MyService"""
#   def __init__(self, cfg):
#       super( MyService, self).__init__()
#       self.cfg = cfg
#       self.data = 0

#   def inc_data(self):
#       self.data += 1

#   @property
#   def data(self):
#       return self.data




@decorators.as_service(name="ASuperServ",config_path="OfObjects.UnServiceUtilisateur")
class MyService(object):
    """docstring for MyService"""
    def __init__(self, cfg):
        super( MyService, self).__init__()
        self.cfg = cfg


@decorators.dependencies( TheDataService='DataService', TheSameDataService='DataService')
def di_user_method_named_args(TheDataService=None,TheSameDataService=None):
    return TheDataService.data == TheSameDataService.data


@decorators.dependencies( 'TheDataService=DataService', 'TheSameDataService=DataService')
def di_user_method_formated_args(TheDataService=None,**kwargs):
    return TheDataService.data == kwargs.get('TheSameDataService').data


@decorators.dependencies( 'DataService')
@decorators.dependencies( 'TheDataService=DataService')
def di_user_method_service_name(TheDataService=None,**kwargs):
    return TheDataService.data == kwargs.get('DataService').data


@decorators.dependencies( 'TheDataService=DataService', 'DataService')
class DiUserClassWithServiceName(object):
    def __init__(self,TheDataService=None,**kwargs):
        self.TheDataService = TheDataService
        self.DataService    = kwargs.get('DataService')

    def check(self):
        return self.TheDataService.data == self.DataService.data


class TestDecorators(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dependency_injection_inside_methodes(self):
        assert di_user_method_named_args()    == True
        assert di_user_method_formated_args() == True
        assert di_user_method_service_name()  == True


    def test_dependency_injection_inside_classes(self):
        assert DiUserClassWithServiceName().check() == True




# if __name__ == '__main__':
#     unittest.main()
