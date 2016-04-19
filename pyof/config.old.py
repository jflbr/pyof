
_default_cfg_file = "/Users/jfl/Documents/Workspaces/Repositories/pyof/pyof/application.json"

class Config(object):
    """An object configuration dict"""
    def __init__(self, cfg=dict()):
        super(Config, self).__init__()
        self.cfg = cfg
        self.owner_name = ''
        self._current = 0
        self._top_size = len(self.cfg)


    def __str__(self):
        return str(self.cfg)

    def __iter__(self):
        self._current=0
        return self

    def next(self):
        if self._current >= self._top_size:
            raise StopIteration
        self._current += 1
        return self.cfg.items()[self._current - 1] 


    def _get_sub_value(self,dotted_item):
        item_path = [ item.strip() for item in dotted_item.split('.')]

    def get_value(self,item):
        return self.cfg.get( item, None )

    def get_abs_value(self,item,required=False):
        item_path = item.split('.')
        value = None
        path_entry = self.cfg
        for key in item_path:
            value = path_entry.get( key, None )
            path_entry = value

            if value is None and required:
                raise errors.ItemNotFound('{0}.{1}'.format(self.owner_name, item))

            if not isinstance(path_entry,dict):break
        return value




class GlobalConfig(Config):
    """docstring for GlobalConfig"""
    def __init__(self, cfg):
        super (GlobalConfig, self).__init__(cfg)





class ConfigReader(object):
        """docstring for base ConfigReader"""
        PATH_SEP = '.'

        def __init__(self):
            super(ConfigReader, self).__init__()
            self.cfg_file_dict  = {}

        def setup(self):
            '''
                In case of remote configuration
            '''
            pass


        def item_node(self,item,required=False):
            item_path = item.split('.')
            value = None
            path_entry = self.cfg_file_dict
            for key in item_path:
                value = path_entry.get( key, None )
                path_entry = value

                if (value is None) and (required is True) or (not isinstance(path_entry,dict)):
                    raise errors.NotAConfigNode('{0}.{1}'.format(self.owner_name, item))

                if not isinstance(path_entry,dict):break
            return GlobalConfig( value )


        @property
        def global_config(self):
            return GlobalConfig( self.cfg_file_dict )

        def object_config(self,object_name):
            object_cfg = Config( self.cfg_file_dict.get(object_name) )
            object_cfg.owner_name = object_name
            return object_cfg

        @property
        def internal_data(self):
            return self.cfg_file_dict


class LocalConfigReader(ConfigReader):
    """docstring for LocalConfigReader"""
    def __init__(self, cfgFile=_default_cfg_file ):
        self.cfg_file       = cfgFile
        super(LocalConfigReader, self).__init__()


        try:
            with open(self.cfg_file, 'r') as raw_cfg:
                self.cfg_file_dict = json.load(raw_cfg)
        except Exception as e:
            print 'Unable to read the configuration file\n\t>>> File : {0}\
            \n\t>>> Error: {1}'.format(self.cfg_file,e)


