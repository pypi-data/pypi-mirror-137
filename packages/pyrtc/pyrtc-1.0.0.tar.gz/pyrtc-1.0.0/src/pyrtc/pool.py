import uuid

from .transceiver import Transceiver, TransceiverManager

class Pool:
	def __init__(self, name, timeout=30):
		"""
		Create a pool with the given unique name and timeout.
		timeout is the number of seconds after which a pool will
		automatically close without activity.
		"""
		self._name = name
		self._conns = {}
		self._closed = False
		self.timeout = timeout

	def get_peer_ids(self):
		"""
		Returns a tuple of the IDs of all connected peers.
		"""
		return tuple(self._conns.keys())

	@property
	def name(self):
		return self._name

	@property
	def closed(self):
		return self._closed

	def allows(self, endpoint):
		"""
		A method which returns a boolean
		value telling whether the given
		endpoint is allowed to join this
		pool. Subclasses may return False
		in some cases, blocking certain
		endpoints from joining.
		"""
		return not self.closed

	def get_connection(self, test):
		"""
		If test is a string, gets a connection by its ID.
		If test is a Transceiver, gets the connection associated with it.
		If no connection is found, None is returned.
		"""
		if isinstance(test, str):
			return self._conns.get(test, None)
		elif isinstance(test, Transceiver):
			for i in self._conns.values():
				if i['socket'] == test:
					return i
			return None
		else:
			raise TypeError("get_connection accepts a UUID string or a Transceiver.")

	def add_endpoint(self, transceiver):
		"""
		Accepts a Transceiver and adds it to the pool
		as an endpoint.
		"""
		if transceiver in self:
			raise ValueError("This endpoint has already been added!")

		ent = {
			'socket': transceiver,
			'id': str(uuid.uuid4()),
			'description': None
		}

		self._conns[ent['id']] = ent
		return ent

	def update(self):
		"""
		Prunes closed connections and notifies peers of the closure.
		"""
		if self.closed: return

		# remove closed transceivers,
		# send close notifications to peers
		pre_load = tuple(self._conns.values())
		closed = []
		for conn in pre_load:
			if not conn['socket'].is_open():
				closed.append(conn['id'])
				del self._conns[conn['id']]

		for c in closed:
			self.broadcast('rtc:close', { 'uid': c })

	def describe(self, id_or_trans, desc):
		"""
		Sets the description of the specified connection.
		"""
		if self.closed:
			raise ValueError("Pool is closed")

		assert desc is None or isinstance(desc, dict)
		conn = self.get_connection(id_or_trans)
		if conn:
			self.broadcast('rtc:describe', {
				'description': desc,
				'uid': conn['id']
			})

	def broadcast(self, evt_type, evt_data, *exclude):
		"""
		Broadcasts the specified event to all connections in the pool,
		except for those whose Transceiver is in ``exclude``.
		"""
		if self.closed:
			raise ValueError("Pool is closed")

		for conn in filter(lambda ent: ent['socket'] not in exclude, self._conns.values()):
			conn['socket'].send(evt_type, evt_data)

	def close(self):
		"""
		Sends a signal to close all connections in the pool,
		and closes the signalling channels.
		"""

		if self.closed:
			raise ValueError("Pool is closed")

		self.broadcast('rtc:stop', {})
		for conn in self._conns:
			conn['socket'].close()

		self._conns[:] = []
		self._closed = True

	def __contains__(self, test):
		if isinstance(test, str):
			# check by UID
			return test in self._conns.keys()
		elif isinstance(test, Transceiver):
			return test in map(lambda ent: ent['socket'], self._conns.values())
		else:
			return False

class PoolManager:
	def __init__(self, private=True):
		self._private = private
		self._pools = []
		self._trans = TransceiverManager()

		self._closed = False

	def close(self):
		"""
		Closes this pool manager.
		"""
		self._trans.close_all()
		self._closed = True

	def _close_assert(self, msg="PoolManager is closed"):
		assert not self._closed, msg

	def update(self):
		self._close_assert()
		for event, source in self._trans.events():
			self.handle_event(event, source)

		immut = tuple(self._pools)
		for pool in immut:
			if pool.closed:
				self._pools.remove(pool)
			else:
				pool.update()

	def add_endpoint(self, transceiver):
		self._close_assert()
		self._trans.dispatch(transceiver)

	def add_pool(self, pool):
		self._close_assert()
		if pool.name in map(lambda pool: pool.name, self._pools):
			raise ValueError(f"Pool with name '{pool.name}' already exists!")
		else:
			self._pools.append(pool)

	def get_pool(self, name):
		for pool in self._pools:
			if pool.name == name: return pool

		return None

	def remove_pool(self, name):
		self._close_assert()
		pool = self.get_pool(name)
		if pool is not None:
			self._pools.remove(pool)
			return True
		else:
			return False

	def _query(self, test):
		for pool in self._pools:
			conn = pool.get_connection(test)
			if conn:
				return pool, conn

		return None, None

	def get_pool_for(self, test):
		return self._query(test)[0]

	def get_connection_for(self, test):
		return self._query(test)[1]

	def handle_event(self, event, source):
		"""
		:param: event
		:type event: tuple
		:param source:
		:type source: Transceiver
		"""

		self._close_assert()

		name, data = event
		parts = name.split(':')
		prefix = parts[0]
		if prefix != 'rtc' or len(parts) != 2:
			# Ignore events not intended for the rtc
			# signalling process. This allows a single
			# websocket to be used for RTC signalling
			# as well as other applications.
			return

		action = parts[1]
		if action == 'join':
			_pool = data.get('pool', None)
			if not _pool:
				source.send('rtc:error', {
					'message': 'Please specify a pool to join.'
				})
			pool = self.get_pool(_pool)

			if pool:
				can_join = pool.allows(source)
				if can_join:
					peers = pool.get_peer_ids()
					result = pool.add_endpoint(source)
					source.id = result['id']
					joined = ('rtc:joined', {
						'client_id': result['id'],
						'peers': peers,
						'pool': pool.name
					})
				else:
					source.send('rtc:error', {
						'message': 'You are not authorized to join.',
						'pool': pool.name
					})
					return
			else:
				if self._private:
					# pools cannot be created implicitly,
					# must be explicitly created by server code
					source.send('rtc:error', {
						'message': 'No such pool exists.',
						'pool': _pool
					})
					return
				else:
					# auto-add default pool
					pool = Pool(_pool)
					self.add_pool(pool)
					peers = pool.get_peer_ids()
					ent = pool.add_endpoint(source)
					source.id = ent['id']
					joined = ('rtc:joined', {
						'client_id': ent['id'],
						'peers': peers,
						'pool': pool.name
					})

			# if we get here, joined will have been assigned
			source.send(*joined)
			pool.broadcast("rtc:request_offers", {
				"for": source.id
			}, source)
		elif action == 'offers':
			for key in data.keys():
				pool, conn = self._query(key)
				if conn:
					conn['socket'].send('rtc:offer', {
						'for': source.id,
						'offer': data[key]
					})
		elif action == 'answer':
			target = data.get('for', None)
			if target:
				conn = self.get_connection_for(target)
				if conn:
					conn['socket'].send('rtc:answer', {
						'for': source.id,
						'answer': data.get('answer')
					})
			else:
				source.send('rtc:error', {
					'message': 'Please specify an answer target.'
				})
		elif action == 'candidate':
			target = data.get('for', None)
			if target:
				conn = self.get_connection_for(target)
				if conn:
					conn['socket'].send('rtc:candidate', {
						'candidate': data.get('candidate'),
						'from': source.id
					})
			else:
				source.send('rtc:error', {
					'message': "Please specify a candidate recipient in the 'for' field."
				})
		else:
			source.send('rtc:error', {
				'message': f"RTC action '{action}' not recognized."
			})