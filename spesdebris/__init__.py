import configparser
import logging
import socket
import time
from sys import exit

import paramiko
from win10toast import ToastNotifier

from dbxhandler import DropboxHandler
from fcmhandler import FCMHandler
from extrq import RequestProcessor
from server import Server


config = configparser.ConfigParser()
config.read('settings.ini')

port = config.getint('Server', 'Port')
toaster = ToastNotifier()
dbh = DropboxHandler(
    config.get('APIkeys', 'Dropbox'),
    toaster
)
fcmh = FCMHandler(
    config.get('Client', 'Account'),
    config.get('APIkeys', 'Automate')
)
reqproc = RequestProcessor(
    dbh, fcmh, toaster
)

logging.basicConfig()
logger = logging.getLogger()


def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))

    sock.listen(100)
    client, addr = sock.accept()
    print(
        f"[{time.strftime('%H:%M:%S', time.localtime(time.time()))}"
        f"] Incoming connection from {addr}"
    )

    t = paramiko.Transport(client)
    t.set_gss_host(socket.getfqdn(""))
    t.load_server_moduli()
    server = Server(
        config.get('Server', 'PublicKeyFile'),
        config.get('Server', 'PrivateKeyFile'),
        reqproc,
        config.get('Server', 'Username')
    )
    t.add_server_key(server.host_key)
    t.start_server(server=server)

    # Wait 30 seconds for a command
    server.event.wait(30)
    t.close()
    print("Connection closed\n")

def cleanup():
    exit(0)

def daemon_mode(args):
    print(
        "spesdebris daemon started\n"
        f"Starting SSH server on port {port}\n"
    )
    while True:
        try:
            listener()
        except KeyboardInterrupt:
            print("spesdebris daemon stopped")
            cleanup()
        except Exception as exc:
            logger.error(exc)


def upload_to_phone(args):
    if not args.source_file:
        raise Exception("Error: the source file is not specified")

    file_name = args.source_file.split("\\")[-1]
    upload_result = dbh.upload_file(
        local_path=args.source_file,
        remote_path=None
    )

    fcmh.send_message(
        device=config.get('Client', 'Device'),
        payload={
            "command": "Get file",
            "from": upload_result.link,
            "to": args.destination or config.get(
                'Client', 'DefaultDownloadFolder') + file_name,
            "filename": file_name
        }
    )

    cleanup()


def send_fcm_message(args):
    fcmh.send_message(
        device=config.get('Client', 'Device'),
        payload={
            "command": "Show message",
            "message": args.message
        }
    )

    cleanup()