import etcd
import config
import json
from services import Backend, Service
moduleLogger = config.getLogger('etcd')

def etcdClientConfig():
	clientConfig = {
		'host': config.ETCD_HOST,
		'port': config.ETCD_PORT
	}
	return clientConfig

def createClient():
	return etcd.Client(**etcdClientConfig())

etcdClient = createClient()

def getServices(services = {}):
	try:
		raw = etcdClient.read(config.ETCD_ROOT_KEY, recursive = True, sorted=True)
	except:
		moduleLogger.error('Failed to connect to etcd host %s:%s'%(config.ETCD_HOST, config.ETCD_PORT))
		return services

	rawServices = [x for x in raw.get_subtree() if x.dir and not x.key == config.ETCD_ROOT_KEY ]
	for service in rawServices:
		# split the key to obtain the service name
		name = service.key[1:].split('/')[1]
		# load the available backends
		try:
			backends = [Backend(**json.loads(x.value)) for x in service.leaves]
		except:
			backends = []

		if backends:
			# retrieve service if it already exists otherwise create a new one
			s = services.get(name, Service(name))

			for back in backends:
				s.addBackend(back)

			services[name] = s
		else:
			moduleLogger.debug('No backends found for service %s not including in list'%name)

	return services
