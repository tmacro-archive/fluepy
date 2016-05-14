import dns.update
import dns.query
import dns.tsigkeyring
from socket import gethostbyname
import config

def loadKey():
	if isinstance(config.RNDC_KEY, dict):
		return dns.tsigkeyring.from_text(config.RNDC_KEY)
	else:
		raise Exception('Invalid tsig key')


def updateDNS(services):
	update = dns.update.Update(config.DNS_ZONE, keyring=loadKey())
	for service in services:
		for backend in service.backends:
			update.replace(service.name, config.RECORD_TTL, 'A', gethostbyname(backend.host))
	return dns.query.tcp(update, gethostbyname(config.DNS_HOST), timeout=10)
