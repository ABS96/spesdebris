import configparser
import logging
import socket
import sys

import paramiko

from extrq import RequestProcessor
from server import Server

config = configparser.ConfigParser()
config.read('settings.ini')

port = config.getint('Server','Port')

reqProc = RequestProcessor(
	config.get('APIkeys','Dropbox'),
	config.get('Client','Account'),
	config.get('APIkeys','Automate')
)

logging.basicConfig()
logger = logging.getLogger()

def listener():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', port))

	sock.listen(100)
	client, addr = sock.accept()
	print(f"Incoming connection from {addr}")

	t = paramiko.Transport(client)
	t.set_gss_host(socket.getfqdn(""))
	t.load_server_moduli()
	server = Server(
		config.get('Server','PublicKeyFile'),
		config.get('Server','PrivateKeyFile'),
		reqProc
	)
	t.add_server_key(server.host_key)
	t.start_server(server=server)

	# Wait 30 seconds for a command
	server.event.wait(30)
	t.close()
	print("Connection closed\n")

print(f"Starting SSH server on port {port}\n")
while True:
	try:
		listener()
	except KeyboardInterrupt:
		sys.exit(0)
	except Exception as exc:
		logger.error(exc)