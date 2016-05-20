import pull
import push
from time import sleep
import config
moduleLogger = config.getLogger('flue')

services = {} #change to dict
while True:
	moduleLogger.debug('Watching %s for registered services'%config.ETCD_ROOT_KEY)
	updated = pull.getServices(services)
	if updated == None:
		continue
	removed = []
	for name, service in services.items():
		if not name in updated:
			removed.append(name)

	# moduleLogger.debug(updated, removed)
	push.updateDNS(updated, removed)

	services = updated

	sleep(config.POLL_TIME)
