from config import ConfigReader, Config, LocalConfigReader
from errors import UnregisteredClass,AlreadyRegisteredClass,RegistryError





class Registry(object):
    """docstring for Registry"""
    def __init__(self, *arg,**kwargs):
        super(Registry, self).__init__()
        self.arg = arg

        self.instances = {'static':{ },'dynamic':{ }}
        self.classes   = {} #key=of_name,value=others
        # class  { 'params': None,'instance': None, 'path': None , shared=False, static=True,'cls': None }


    def is_registered(self,of_name):
        return self.classes.has_key(of_name)


    def register_static_class(self,of_name,cls,params=dict(),shared=False):
        if None != self.classes.get('of_name') :
            raise AlreadyRegisteredClass(of_name)
        self.classes[of_name]={ 'params': params,'instance': None, 'path': None , 'shared':shared, 'static':True,'cls': cls }

    def is_static(self,of_name):
        return self.classes[of_name].get('static')

    def is_shared(self,of_name):
        return self.classes[of_name].get('shared')


    def register_config_class(self,of_name,path,params=dict(),shared=False):
        if None != self.classes.get('of_name') :
            raise AlreadyRegisteredClass(of_name)
        self.classes[of_name]={ 'params': None,'instance': None, 'path': path , 'shared':shared, 'static':False,'cls': None }

    def get_object_class(self, of_name):
        return self.get_static_class(of_name)


    def get_static_class(self, of_name):
        try:
            return self.classes.get(of_name).get('cls',None)
        except:
            raise UnregisteredClass(of_name)

    def get_class_config(self, of_name):
        try:
            return self.classes[of_name]
        except:
            raise UnregisteredClass(of_name)

    def is_shared(self, of_name):
        try:
            return self.classes.get(of_name).get('shared')
        except:
            raise UnregisteredClass(of_name)

    def get_config_class(self, of_name):
        try:
            return self.classes.get(of_name).get('path',None)
        except:
            raise UnregisteredClass(of_name)

    def set_object_instance(self,name,instance):
        try:
            assert self.classes.get(name,{}).get('shared',False) == True
        except AssertionError:
            raise RegistryError("Class {} is not shared but an instance was provided".format(name))
        else:
            self.classes[name]['instance']=instance

    def object_instance(self,name,static=True):
        return self.get_instance(name,static)

    def get_instance(self,name,static=True):
        try:
            assert self.classes.get(name,{}).get('shared',False) == True
        except AssertionError:
            raise RegistryError("Class {} is not shared but an instance was provided".format(name))
        return self.instances.get(name,{}).get('instance',None)


class Factory(object):
    """docstring for Factory"""
    service_pattern = { 'instance': None, 'path': None ,'instanciated':False }

    registry        = Registry()
    config_reader   = LocalConfigReader()

    #Static registration of DataService...
    registered_services = {} # {  'DataService': { 'instance':DataService(), 'path': 'a_path_to_a_config_node' ,'instanciated':True  }  }

    @staticmethod
    def register_config_service(name,path):
        #service = Factory.service_pattern.copy()
        registry.register_config_class(name,path=path,shared=True)

        #service['path']=path
        #if Factory.registered_services.get( name , None) is None:
        #    Factory.registered_services[ name ] = service

    @staticmethod
    def register_config_class(name,path,shared=False):
        #service = Factory.service_pattern.copy()
        registry.register_config_class(name,path=path,shared=shared)


    @staticmethod
    def register_user_class(name,cls,parameters,shared=False):
        Factory.registry.register_static_class(of_name=name,cls=cls,params=parameters,shared=shared)

    @staticmethod
    def obtain_object_config(path):
        return Factory.config_reader.get_config(path)


    @staticmethod
    def obtain_object( object_name ) : #, service=False, meta=False ):
        # print 'Return a static object...'
        # return Factory.registered_services.get('DataService').get('instance')
        #instance().obtain_object(object_name)
        if Factory.registry.is_registered( object_name ):
            print 'Object {} is registered!'.format( object_name )

        else:
            print 'Object {} is not registered!'.format( object_name )
            return


        #if service:
        #Config object construction
        if not Factory.registry.is_static( object_name ):
            print "COOOOOONFFFFFIIIIIIG"
            try:
                #config = Factory.registered_services.get(object_name,None)
                config = Factory.registry.get_class_config(object_name)

                if config is None : raise ValueError('Factory - Can not obtain service < {} >. Not registered'.format(object_name))
                if config.get('instance') is None:
                    #config['instance'] = Factory.createObject(config.get('path'))
                    pass
                return config.get('instance')
            except:
                raise ValueError('Factory - Can not obtain service < {} >. Not registered'.format(object_name))
        else:
            print "STAAAAAAATIIIIIIC"
            #Staic instanciation
            object_cls = Factory.registry.get_object_class(object_name)
            instance   = Factory.registry.object_instance( object_name,static=True)

            if Factory.registry.is_shared(object_name):
                if  instance is None:
                    instance = object_cls()
                    Factory.registry.set_object_instance( object_name, instance )
            else:
                instance = object_cls()

            return instance


            #Factory.registry.get_object_class(object_name)
            # try:
            #     return Factory.new_object(object_name)
            # except Exception, e:
            #     raise e

    @staticmethod
    def new_object( objectName ):
        try:
            object_params = Factory.obtain_object_config(objectName)
        except KeyError:
            print 'Object "{0}" is not declared in the configuration file'.format( objectName )
            return

        instanceOf = object_params.get_value('InstanceOf')
        parts      = instanceOf.split('.')
        module_name= ".".join( parts[ :-1] )
        m          = __import__( module_name )

        for sub_item in parts[1:]:
            m = getattr( m, sub_item )
        #self.instances_map[ objectName ] = m( object_params )
        return m( cfg=object_params )



    def __init__(self, arg):
        super(Factory, self).__init__()
        self.arg = arg




if __name__ == '__main__':
    pass



    #Registry().get_config_class("meta.RemoteTraceMonitor")
