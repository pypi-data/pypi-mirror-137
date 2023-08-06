from abc import ABC, abstractmethod

from . import transport

class Transceiver(ABC):
	def __init__(self):
		self.id = None

	@abstractmethod
	def is_open(self):
		"""
	`	A method used to check whether the channel
		used to transmit and received data is open.
		"""
		return True

	@abstractmethod
	def send(self, event_type, event_data):
		"""
		A method which sends an event to an endpoint. How the
		data is sent or formatted is defined by individual
		subclasses and is not important as long as it sent somehow.

		:param event_type: The type of event to be processed.
		:type event: str
		:param event_data: Data describing the event.
		:type event_data: dict
		"""
		pass

	@abstractmethod
	def receive(self):
		"""
		A generator yielding all relevant events at the time it is called.

		Events should be yielded as a 2-tuple (event_type, event_data)
		"""
		pass

	@abstractmethod
	def close(self):
		pass

class WebsocketTransceiver(Transceiver):
	def __init__(self, ws):
		super().__init__()
		if not isinstance(ws, transport.Websocket):
			raise TypeError("ws must be a Websocket instance!")
		else:
			self._ws = ws
			self._recv = transport.EventReceiver()
			self._ws.add_receiver(self._recv)

	def is_open(self):
		return self._ws.open

	def send(self, event_type, event_data):
		self._ws.send(transport.create_event(event_type, event_data))

	def receive(self):
		self._ws.receive()
		yield from self._recv

	def close(self):
		self._ws.close_raw()

	@property
	def socket(self):
		return self._ws

	@staticmethod
	def of(raw_sock):
		porter = transport.Websocket(raw_sock)
		return WebsocketTransceiver(porter)

class TransceiverManager:
	def __init__(self):
		self._trans = []

	def dispatch(self, transceiver):
		self._trans.append(transceiver)

	def events(self):
		"""
		Used by PoolManager to receive all events from all
		transceivers and handle them.
		"""
		for trans in self._trans:
			for event in trans.receive():
				yield (event, trans)

		self._trans[:] = [trans for trans in self._trans if trans.is_open()]

	def close_all(self):
		for trans in self._trans:
			trans.close()

		self._trans = []