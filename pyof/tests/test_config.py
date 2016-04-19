#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
----------------------------------
Tests for `config` module.
"""

import unittest
from .. import config


class TestConfig(unittest.TestCase):


    def setUp(self):

        self.config_reader = config.LocalConfigReader()
        self.config        = self.config_reader.get_config( 'OfObjects.Sasuke' )


    def tearDown(self):
        pass

    def test_get_value(self):
        #With some existing values...
        assert self.config.get_value('level')==100
        assert self.config.get_value('Objects.shortweapon.damage') == 10

    def test_get_wrong_value(self):
        self.assertRaises( ValueError, self.config.get_value, 'aValueThatDoes.Not.Exist' )
        self.assertRaises( ValueError, self.config.get_value, 'aValueThatDoes.Not.Exist' ,required=True)
        assert self.config.get_value( 'aValueThatDoes.Not.Exist' , required=False)==None


    def test_wrong_config_path(self):
        self.assertRaises( ValueError, config.LocalConfigReader().get_config, 'aValueThatDoes.Not.Exist' )
        self.assertRaises( ValueError, config.LocalConfigReader().get_config, 'aValueThatDoes.Not.Exist' , required=True)
        assert config.LocalConfigReader().get_config( 'aValueThatDoes.Not.Exist' , required=False)==None

    def test_attributes(self):
        #Config name
        assert 'Sasuke' == self.config.name
        #Config path (absolute)
        assert 'OfObjects.Sasuke' == self.config.path

    def test_set_value(self):

        self.config.set_value('Objects.shortweapon.damage', 15)
        assert self.config.get_value('Objects.shortweapon.damage') ==  15
        assert self.config_reader.get_value('OfObjects.Sasuke.Objects.shortweapon.damage') ==  15
        self.config_reader.set_value('OfObjects.Sasuke.Objects.shortweapon.damage', 22 )
        assert self.config.get_value('Objects.shortweapon.damage') ==  22


    def test_get_abs_name(self):
        assert self.config.get_abs_name("level") == "OfObjects.Sasuke.level"


    def test_store(self):
        self.config.set_value('Objects.shortweapon.damage', 2000)
        self.config_reader.store('examples/test_store_with_OfObjects.Sasuke.Objects.shortweapon.damage_value_is_2000.json')
        self.config.set_value('Objects.shortweapon.damage', 5000)
        self.config_reader.store('examples/test_store_with_Sasuke.shortweapon.damage_is_5000.json' )
