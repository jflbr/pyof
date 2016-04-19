#! /usr/bin/python

# -*- coding:utf-8 -*-
#from __future__ import absolute_import
import json
#import pprint

#from . import errors
#import errors


_default_cfg_file = "/Users/jfl/Documents/Workspaces/Repositories/pyof/pyof/application.json"



class ConfigListener(object):
    def __init__(self):
        pass
    def newData(self,data):
        pass


class Config(ConfigListener):
    """An object configuration dict"""
    def __init__(self, path=None, data=dict()):
        super(Config, self).__init__()

        if  not type(data) == dict or path == None:
            raise ValueError('Config - Invalid parameters (data or path)'.format(path) )

        self.data = data
        self.name = path.split(ConfigReader.PATH_SEP)[-1]
        self.path = path

        self._current = 0
        self._top_size = len(self.data)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        self._current=0
        return self

    def next(self):
        if self._current >= self._top_size:
            raise StopIteration
        self._current += 1
        return self.data.items()[self._current - 1]

    @property
    def values(self):
        for element in  self.data:
            yield element

    def set_value(self,path,obj):
        if self.is_valid(path):
            #target = ConfigReader.PATH_SEP.join( path.split( ConfigReader.PATH_SEP )[:-1] )
            #self.get_value( target )[ path.split( ConfigReader.PATH_SEP)[-1] ] = obj
            path_list = path.split( ConfigReader.PATH_SEP )
            reduce( dict.get,path_list[:-1],self.data )[path_list[-1]] = obj
            #reduce( dict.get, obj, path.split(ConfigReader.PATH_SEP), self.data )
        else:
            raise ValueError('Path <{}> does not exist'.format(path) )


    def get_value(self, path,required=True):
        if self.is_valid(path):
            return reduce( dict.get,path.split( ConfigReader.PATH_SEP ), self.data )
        elif required:
            raise ValueError( 'Path <{}> does not exist'.format(path) )
        return None


    def get_abs_name(self,rel_name):
        return self.get_item_path( rel_name )


    def get_item_path(self,key_name):
        if self.is_valid(key_name):
            #print '"{}" is valid!'.format(key_name)
            return ConfigReader.PATH_SEP.join( [self.path, key_name] )
        else:
            raise ValueError( 'Item <{}> does not exist in this configuration node'.format(key_name) )



    def is_valid(self,path):
        ''' check whether the given path is valid in the local configuration '''
        res = True
        try:
            if reduce( dict.get,path.split(ConfigReader.PATH_SEP), self.data) is None:
                res = False
        except:
            res = False
        return res

    def newData(self,data):
        self.data.clear()
        self.data.update( data )





class ConfigReader(object):
        """docstring for base ConfigReader"""
        PATH_SEP = '.'


        def __init__(self):
            super(ConfigReader, self).__init__()
            self.config_dict      = {}
            self.config_listeners = []


        def setup(self):
            '''
                In case of remote configuration
            '''
            pass

        def object_config(self,object_name):
            object_cfg = Config( self.config_dict.get(object_name) )
            object_cfg.owner_name = object_name
            return object_cfg

        @property
        def internal_data(self):
            return self.config_dict


        def get_config(self,path,required=True, is_listener=False):
            try:
                cfg = Config( path=path, data=self.get_value(path) )
                if is_listener:
                    self.config_listeners.append(cfg)
                return cfg
            except ValueError :
                if required:
                    raise ValueError("Path <{}> is not a configuration node".format(path))



        @property
        def entries(self):
            for element in  self.config_dict:
                yield element


        def set_value(self,path,obj):
            if self.is_valid( path ):
                path_list = path.split( ConfigReader.PATH_SEP )
                reduce( dict.get,path_list[:-1],self.config_dict )[path_list[-1]] = obj
            else:
                raise ValueError('Path <{}> does not exist'.format(path) )


        def get_value(self, path):
            if self.is_valid(path):
                return reduce( dict.get,path.split(ConfigReader.PATH_SEP), self.config_dict)
            else:
                raise ValueError('Path <{}> does not exist'.format(path) )



        def is_valid(self,path):
            ''' check whether the given path is valid in the local configuration '''
            res = True
            try:
                reduce( dict.get,path.split(ConfigReader.PATH_SEP), self.config_dict)
            except:
                res = False
            return res






class LocalConfigReader(ConfigReader):
    """docstring for LocalConfigReader"""
    def __init__(self, cfgFile=_default_cfg_file ):
        self.config_file       = cfgFile
        super(LocalConfigReader, self).__init__()

        try:
            with open(self.config_file, 'r') as raw_cfg:
                self.config_dict = json.load(raw_cfg)
        except Exception as e:
            print 'Unable to read the configuration file\n\t>>> File : {0}\
            \n\t>>> Error: {1}'.format(self.config_file,e)


    def store(self,cfg_file=None):
        try:
            if cfg_file:
                target_file_name = cfg_file
            else :
                target_file_name = self.config_file

            with open(target_file_name, 'w') as target_file:
                json.dump( self.config_dict, target_file ,indent=4)
        except Exception as e:
            print 'Unable to open the configuration file\n\t>>> File : {0}\
            \n\t>>> Error: {1}'.format(self.config_file,e)


        def reload(self):
            pass


#
# Dummy code to make some quick 'tests'
#

def main():
    #pprint.pprint( LocalConfigReader().internal_data.get('Sasuke').get('AutoCreate') )
    #print dir(LocalConfigReader().internal_data.get('Sasuke'))
    for x,y in LocalConfigReader().get_config('OfObjects.Sasuke') : print x,' : ',y
    print 'OfObjects.Sasuke.ComposedOf - ',LocalConfigReader().get_config('OfObjects.Sasuke').get_value("ComposedOf")


    print  'Sasuke.Objects.shortweapon : {0}'.format(LocalConfigReader().get_config('OfObjects.Sasuke').get_value('Objects.shortweapon',required=False))



if __name__ == '__main__':
    main()
