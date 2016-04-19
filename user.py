from pyof import decorators 
from pyof import factory


@decorators.dependencies('caller=my_function')
def my_function(**kwargs):
	pass


@decorators.as_service(name="ASuperServ",config_path="App.Services.Mine")
class MyService(object):
	"""docstring for MyService"""
	def __init__(self, cfg):
		super( MyService, self).__init__()
		self.cfg = cfg



if __name__ == '__main__':
	print '>>> Factory.decorated   : ',factory.Factory.decorated
	print '>>> Factory.reg_services: ',factory.Factory.registered_services
