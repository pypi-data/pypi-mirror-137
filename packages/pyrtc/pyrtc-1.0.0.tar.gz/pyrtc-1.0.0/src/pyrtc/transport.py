import json

import select
import socket
import ssl

from wsproto import events, ConnectionType, WSConnection
from wsproto.connection import ConnectionState

def can_read(sock):
	if isinstance(sock, ssl.SSLSocket):
		return sock.pending() > 0
	else:
		return sock in select.select([sock], [], [], 0)[0]

def can_write(sock):
	# should work for both SSL and non-SSL sockets
	return sock in select.select([], [sock], [], 0)[1]

def create_event(name, data):
	return events.TextMessage(json.dumps({
		'type': name,
		'data': data
	}))

class EventReceiver:
	def __init__(self):
		self._buffer = []

	def __iter__(self):
		return self

	def __next__(self):
		if len(self._buffer) > 0:
			return self._buffer.pop(0)
		else:
			raise StopIteration

	def post(self, evt):
		self._buffer.append(evt)

	@property
	def pending(self):
		return len(self._buffer)

class Websocket:
	def __init__(self, cli_sock):
		self._sock = cli_sock
		self._conn = WSConnection(ConnectionType.SERVER)
		self._closed = False
		self._receivers = []

	def add_receiver(self, receiver):
		if isinstance(receiver, EventReceiver):
			self._receivers.append(receiver)
		else:
			raise TypeError("receiver must be an instance of EventReceiver")

	def _raw_send(self, data):
		if self._sock.fileno() == -1:
			self._closed = True
			return

		sent = 0
		while sent < len(data):
			if can_write(self._sock):
				try:
					sent += self._sock.send(data[sent:])
				except socket.error:
					# broken pipe
					self._closed = True
					return
			else:
				time.sleep(0.05)

	@property
	def open(self):
		return self._conn.state == ConnectionState.OPEN and not self._closed

	def close(self, status=1000):
		if self._conn.state != ConnectionState.OPEN:
			raise ValueError("WebSocket not in the OPEN state.")
		else:
			close = self._conn.send(events.CloseConnection(status))
			self._raw_send(close)
			self._sock.close()

	def close_raw(self):
		if self._conn.state == ConnectionState.OPEN:
			self.close()
		else:
			self._closed = True
			self._sock.close()

	def send(self, data):
		if isinstance(data, str):
			message = events.TextMessage(data)
		elif isinstance(data, bytes):
			message = events.BytesMessage(data)
		elif isinstance(data, (events.TextMessage, events.BytesMessage)):
			message = data
		else:
			raise TypeError("message must be a str or bytes object, or a TextMessage/BytesMessage")

		raw_data = self._conn.send(message)
		self._raw_send(raw_data)

	def receive(self):
		if self._closed:
			return

		while can_read(self._sock):
			data = self._sock.recv(2048)
			if not data:
				# socket closed
				self._closed = True
				return
			self._conn.receive_data(data)

		for event in self._handle(self._conn.events()):
			for recv in self._receivers:
				recv.post(event)

	def _handle(self, event_iter):
		for event in event_iter:
			if isinstance(event, events.Request):
				self._raw_send(self._conn.send(events.AcceptConnection()))
			elif isinstance(event, events.TextMessage):
				if event.message_finished:
					try:
						evt_data = json.loads(event.data)
					except json.decoder.JSONDecodeError:
						# tell client to send valid data!
						self._raw_send(self._conn.send(create_event('rtc:error', { 'message': 'Please send valid JSON data.' })))

					name = evt_data.get('type', None)
					data = evt_data.get('data', None)
					if not (name and isinstance(data, dict)):
						self._raw_send(self._conn.send(create_event('rtc:error', { 'message': 'Please send an event with "type" and "data" fields.' })))
					else:
						yield (name, data)
			elif isinstance(event, events.Ping):
				# send pong, nothing to yield
				self._raw_send(self._conn.send(event.response()))
			elif isinstance(event, events.CloseConnection):
				self.close_raw()
				return
			else:
				# ignore all else
				pass