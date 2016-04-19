
#! /usr/bin/python

# -*- coding:utf-8 -*-

class NotAnOfObject(Exception):
    """docstring for exception NotAnOfObject"""
    def __init__(self, name):
        super(NotAnOfObject, self).__init__("Class <{0}> can not be instanciated from the factory".format(name))

class NotAConfigNode(Exception):
    """docstring for exception NotAConfigNode"""
    def __init__(self, name):
        super(NotAConfigNode, self).__init__("Item <{0}> is not a configuration node".format(name))

class UnregisteredClass(Exception):
    """docstring for exception UnregisteredClass"""
    def __init__(self, name):
        super(UnregisteredClass, self).__init__("Class <{0}> is not registered".format(name))

class AlreadyRegisteredClass(Exception):
    """docstring for exception AlreadyRegisteredClass"""
    def __init__(self, name):
        super(AlreadyRegisteredClass, self).__init__("Class <{0}> is already registered".format(name))

class RegistryError(Exception):
    """docstring for exception RegistryError"""
    def __init__(self, message):
        super(AlreadyRegisteredClass, self).__init__("{}".format(message))


class ItemNotFound(Exception):
            """docstring for ItemNotFound"""
            def __init__(self, name):
                super(ItemNotFound, self).__init__("Item <{0}> is not defined".format(name))
