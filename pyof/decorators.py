
from factory import Factory
from functools import wraps
from types import FunctionType
#alternative: pip install decorator


class dependencies(object):
    '''
         < dependencies > decorator docstrings

        Allows a class to use dependencies by specifying the name of these
        dependencies as dictionnary items.

        Example:
        @dependencies('key0=kAService', key1='AService')
        class AClassThatNeedsSomeDependencies(ABaseClassOrNot):
            def __init__(self, arg0,arg1, key0=None,key1=None,..) [1] or def __init__(self, arg0,arg1, **kwargs ) [2]

            [1] -  Explicit declaration
            [2] -  Dependencies instances will be set inside the dictionnary argument kwargs with keys 'key0' and 'key1'


        Dependencies objects should be registered inside a factory using <as_service> property
        or < as_singleton > property

    '''

    def __init__(self,*args,**kwargs):
        self.args   = args
        self.kwargs = kwargs
        #Factory.decorated.append( args )

    def __call__(self,to_decorate):
        wrapper = self
        abort = (len(self.args)==0) and (len(self.kwargs)==0)
        if abort : raise ValueError('No dependencies provided')

        arg_deps =  [tuple(i.split('=')) for i in wrapper.args if i.find('=')!=-1]
        arg_deps += [(i,i) for i in wrapper.args if i.find('=') == -1]
        dict_deps=  [(k,v) for k,v in wrapper.kwargs.items()]

        deps     = arg_deps + dict_deps
        if not len(deps): raise ValueError('Invalid dependencies format')

        if isinstance( to_decorate, FunctionType):
            @wraps(to_decorate)
            def inner(*args,**kwargs):
                #deps = [tuple(i.split('=')) for i in wrapper.args if i.find('=')!=-1] + [(k,v) for k,v in wrapper.kwargs.items()]

                #Search for dependencies...
                for dep in deps:
                    print "obtain_object {}".format(dep[1])
                    kwargs[ dep[0] ] = Factory.obtain_object( dep[1] ) #, service=True )

                result = to_decorate(*args,**kwargs)
                #Factory.decorated.append( func.__name__ )
                return result
            #decorated = inner

        else:
            class inner(to_decorate):
                #object_config = Factory.obtain_object_config( wrapper.service_config_path )
                def __init__(self,*args,**kwargs):
                    #Search for dependencies...
                    for dep in deps:
                        kwargs[ dep[0] ] = Factory.obtain_object( dep[1] ) #, service=True )
                    super(inner, self).__init__(*args,**kwargs)

        return inner



class injectable(object):
    """docstring for injectable"""
    def __init__(self,name=None,config_path=None,instance_of=None,parameters=None,shared=False):

        # if not config_path and not instance_of:
        #     raise ValueError('@as_service - Missing both the configuration path (config_path) and the service class (instance_of)\
        #         .\n"ONE" of them must be specified')

        self.service_config_path = None
        self.class_name = name #or config_path.split('.')[-1]
        self.class_cfg  = config_path
        self.parameters = parameters
        self.shared        = shared

        self.service_name           = name #or config_path.split('.')[-1]
        self.service_config_path  = config_path
        self.config_path          = config_path
        #Factory.regis
        Factory.registered_services[ name ] = { 'path': self.service_config_path ,'instanciated':False }


    def __call__(self,cls):

        wrapper = self
        #@wraps(cls)
        class inner(cls):
            def __init__(self,*args,**kwargs):
                #inner.__name__ = cls.__name__
                if wrapper.config_path is not None:
                    object_config = Factory.obtain_object_config( wrapper.service_config_path )
                    kwargs['cfg']=object_config

                #super(inner, self).__init__(*args,**kwargs)
                inner.__bases__ = cls.__bases__
                super(inner,self).__init__(*args,**kwargs)
                #cls.__init__(self,*args,**kwargs)

        if self.class_cfg is None:
            if self.class_name is None:
                name = cls.__name__
            else:
                name = self.class_name

            print "USER CLASS REGISTRATION : name = {} and cls = {} and shared={}".format(name,cls,self.shared)

            Factory.register_user_class(name=name,cls=inner,parameters=self.parameters,shared=self.shared)
        else:
            #Config
            pass




        return inner



class as_service(object):
    '''
        < as_service > decorator docstrings
        Allows to register a class (a function, soon :) ) into the main factory.
        Classes declared as services can be injected as dependencies, just by specifying
        the name used to register them as pataremeter of @dependencies property.

        The decorated class should have a dictionanary parameter in which a cfg key will
        allow it to retrieve its configuration items

        ++ TODO: Allow any class to be decorated

        - name : The service name (unique)
        - config_path : absolute path in the configuration file for dynamic instanciation of the actual service
        - instance_of : class to instanciate (static instanciation of the service 'name')

    '''
    def __init__(self,name=None,config_path=None,instance_of=None):

        if not config_path and not instance_of:
            raise ValueError('@as_service - Missing both the configuration path (config_path) and the service class (instance_of)\
                .\n"ONE" of them must be specified')

        self.service_name           = name or config_path.split('.')[-1]
        self.service_config_path  = config_path

        Factory.registered_services[ name ] = { 'path': self.service_config_path ,'instanciated':False }


    def __call__(self,cls):
        wrapper = self

        #@wraps(cls)
        class inner(cls):
            object_config = Factory.obtain_object_config( wrapper.service_config_path )
            def __init__(cfg=object_config):
                super(cls, self).__init__(cfg=cfg)

        return inner



class C(object):
    pass


@injectable(shared=True)
class DataService(C):
    """docstring for DataService, an example of service (static)"""
    def __init__(self, arg="DataService.some_data"):
        print isinstance(self,DataService)
        print type(self)
        print "mro: " ,self.__class__.mro()
        print self.__class__.__name__
        super(DataService, self).__init__()
        #C.__init__(self)

        self.arg = arg

    @property
    def data(self):
        return self.arg



@dependencies( 'TheDataService=DataService', TheSameDataService='DataService' )
def service_user(TheDataService=None,**kwargs):
    print type(TheDataService)
    print  '>>> TheDataService.data     : {}'.format( TheDataService.data )
    return '>>> TheSameDataService.data : {}'.format( kwargs.get('TheSameDataService').data )



def main3():
    print service_user()

if __name__ == '__main__' :
    main3()
    print service_user.__name__
