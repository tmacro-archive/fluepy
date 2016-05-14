import etcd
import config
import json

class Backend(object):
	def __init__(self, host, priority = 0, **kwargs):
		self.host = host
		self.priority = priority

class Service(object):
	def __init__(self, name):
		self.name = name
		self.backends = []

	def addBackend(self, backend):
		self.backends.append(backend)

	def removeBackend(self, backend):
		pass

def etcdClientConfig():
	clientConfig = {
		'host': config.ETCD_HOST,
		'port': config.ETCD_PORT
	}
	return clientConfig

def createClient():
	return etcd.Client(**etcdClientConfig())

etcdClient = createClient()

def getServices():
	services = []
	raw = etcdClient.read(config.ETCD_ROOT_KEY, recursive = True, sorted=True)
	rawServices = [x for x in raw.get_subtree() if x.dir and not x.key == config.ETCD_ROOT_KEY ]
	for service in rawServices:
		name = service.key[1:].split('/')[1]
		backends = [Backend(**json.loads(x.value)) for x in service.leaves]
		s = Service(name)
		for back in backends:
			s.addBackend(back)
		services.append(s)

	return services
