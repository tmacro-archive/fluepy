import dns.update
import dns.query
import dns.tsigkeyring
from socket import gethostbyname
import config
moduleLogger = config.getLogger('ddns')


def loadKey():
	if isinstance(config.RNDC_KEY, dict):
		return dns.tsigkeyring.from_text(config.RNDC_KEY)
	else:
		raise Exception('Invalid tsig key')


def updateDNS(services, removed):
	update = dns.update.Update(config.DNS_ZONE, keyring=loadKey())
	for name in removed:
		moduleLogger.debug('Removing records for nonexistent service %s'%name)
		update.delete(service)


	for name, service in services.items():
		service.diff()
		if service.shouldUpdate():
			moduleLogger.debug('Updating records for %s'%name)
			update.delete(name)

			for backend in service.backends:
				update.add(name, config.RECORD_TTL, 'A', gethostbyname(backend.host))
				moduleLogger.debug('Added record for %s at %s'%(name, backend.host))
		else:
			moduleLogger.debug('No backends for %s have changed NOT updating'%name)

	return dns.query.tcp(update, gethostbyname(config.DNS_HOST), timeout=10)
