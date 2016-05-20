import config
moduleLogger  = config.getLogger('services')

class Backend(object):
	def __init__(self, host, priority = 0, **kwargs):
		self.host = host
		self.priority = priority

	def __eq__(self, other):
		try:
			if self.host == other.host:
				return True
		except:
			pass
		return False

	def __hash__(self):
		return (hash(type(self)) ^ hash(self.host) ^ hash(self.priority))

class Service(object):
	def __init__(self, name):
		self.name = name
		self.backends = set()
		self.added = []
		self.removed = []
		self.last_pushed = 0
		self.changed = True
		self.logger = moduleLogger.getChild(name)

	def __eq__(self, other):
		try:
			if self.name == other.name:
				return True
		except:
			pass
		return False

	def addBackend(self, backend):
		# self.backends.add(backend)
		self.added.append(backend)
		self.logger.debug('Added backend %s'%backend.host)

	def removeBackend(self, backend):
		try:
			backend.remove(backend)
		except:
			pass

	# removes backends that have not been re-added since the last call to diff
	def diff(self):
		self.removed = self.backends - set(self.added)

		numAdded = len(set(self.added)-self.backends)
		numRemoved = len(self.removed)

		merged = self.backends.update(self.added)
		self.backends = self.backends - self.removed

		self.added = []

		if numAdded or numRemoved:
			self.changed = True
		else:
			self.changed = False

		#
		# keep = []
		# for backend in self.backends:
		# 	if not backend in self.added:
		# 		self.removed.append(backend)
		# 		self.logger.debug('Removing backend %s'%backend.host)
		# 	else:
		# 		keep.append(backend)
		# 		self.logger.debug('Keeping backend %s'%backend.host)
		#
		# self.backends = keep
		# self.added = []
		self.logger.debug('Added %i backends - Kept %i backends - Removed %i backend'%(numAdded, len(self.backends)-numAdded, numRemoved))

	def shouldUpdate(self):
		return self.changed
