from config import Config, LocalConfigReader,ConfigReader
from factory import Factory


class CfgObject(object):
    """
        docstring for MetaObject
        A base class with some helper methods to easilly
        access data through a local configuration node
    """

    def __init__(self,*arg,**kwargs):
        super(CfgObject, self).__init__()
        self._config = kwargs.get('cfg',None)


    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, cfg):
        self._config = cfg

    @property
    def objects(self):
        return self._config.get_value("ComposedOf")

    def object_path(self,name):
        return self._config.get_abs_name('Objects.{}'.format(name))

    def get_value(self,key,required=True):
        return self._config.get_value(key,required)

    @property
    def name(self):
        return self._config.name

    @name.setter
    def name(self,_):
        pass


    def type(self,name=None):
        if name in (self.name,None):
            return self._config.get_value('InstanceOf').split(ConfigReader.PATH_SEP)[-1]
        else:
            return self._config.get_value('Objects.{}.InstanceOf'.format(name)).split(ConfigReader.PATH_SEP)[-1]


    def obtain_object(self,name):
        return Factory.obtain_object( self.object_path(name), meta=True)


    def new_object(self,name):
        return Factory.new_object( self.object_path(name), meta=True)




class A(CfgObject):
    """docstring for A"""
    def __init__(self,*arg,**kwargs):
        super(A, self).__init__(*arg,**kwargs)

    def greeting(self):
        print "Hello, world!"



class RemoteTraceMonitor(CfgObject):
    """docstring for A"""
    def __init__(self,*arg,**kwargs):
        super(RemoteTraceMonitor, self).__init__(*arg,**kwargs)

    def level_list(self):
        return self.get_value("traceLevels")




def main():
    #mo=MetaObject()
    #A().greeting()

    # config_reader = LocalConfigReader()
    # config        = config_reader.get_config( 'OfObjects.Sasuke' )

    # mo=A(cfg=config)
    mo=Factory.new_object('OfObjects.Sasuke' )

    trc = Factory.new_object("OfObjects.TraceMonitor")

    print 'Monitor: ',trc.type()
    print 'Level list: ', trc.level_list()
    #mo.config = {'hey':'there!'}
    print mo.config
    print 'objects: ',mo.objects
    print 'shortweapon  path: ', mo.object_path('shortweapon')
    print 'bigweapon  path: ', mo.object_path('bigweapon')
    print 'name: ', mo.name
    print 'level: ', mo.get_value('level')
    print 'AutoCreate: ', mo.get_value('AutoCreate')
    print 'shortweapon type: ', mo.type('shortweapon')


    #a = Factory.new_object('OfObjects.Sasuke' )
    #print 'A.config:', a.config

if __name__ == '__main__':
        main()
