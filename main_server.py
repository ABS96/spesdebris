from base64 import decodebytes
from binascii import hexlify
import configparser
import extrq
import logging
import paramiko
import re
import socket
import sys
import threading

config = configparser.ConfigParser()
config.read('settings.ini')

port = config.getint('Server','Port')

logging.basicConfig()
logger = logging.getLogger()

class Server(paramiko.ServerInterface):
	f = open(config.get('Server','PublicKeyFile'), 'r')
	pub_key_raw = b''
	for line in f.read().split('\n'):
		if re.match(r'----|Comment:|^$',line) == None:
			pub_key_raw += bytearray(line,'utf-8')
	pub_key = paramiko.RSAKey(data=decodebytes(pub_key_raw))

	host_key = paramiko.RSAKey(filename=config.get('Server','PrivateKeyFile'))

	def __init__(self):
		self.event = threading.Event()

	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED

	def check_auth_publickey(self, username, key):
		print("Auth attempt with key: {} by {}".format(hexlify(key.get_fingerprint()).decode('utf-8'),username))
		if (username == "ABS") and (key == self.pub_key):
			print("Auth successful")
			return paramiko.AUTH_SUCCESSFUL
		print("Auth failed")
		return paramiko.AUTH_FAILED

	def get_allowed_auths(self, username):
		return 'publickey'

	def check_channel_exec_request(self, channel, command):
		# This is the command we need to parse
		extrq.process_external_request(command)
		self.event.set()
		return True


def listener():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', port))
	print("Listening on port", port)

	sock.listen(100)
	client, addr = sock.accept()
	print("Incoming connection from",addr)

	t = paramiko.Transport(client)
	t.set_gss_host(socket.getfqdn(""))
	t.load_server_moduli()
	server = Server()
	t.add_server_key(server.host_key)
	t.start_server(server=server)

	# Wait 30 seconds for a command
	server.event.wait(30)
	t.close()

print("Starting SSH server")
while True:
	try:
		listener()
	except KeyboardInterrupt:
		sys.exit(0)
	except Exception as exc:
		logger.error(exc)