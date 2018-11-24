from base64 import decodebytes
from binascii import hexlify
import re
import threading

import paramiko

class Server(paramiko.ServerInterface):

  def __init__(self, pub_key_file, priv_key_file, req_proc):
    self.event = threading.Event()
    self.host_key = paramiko.RSAKey(filename=priv_key_file)
    self.req_proc = req_proc

    f = open(pub_key_file, 'r')
    pub_key_raw = b''
    for line in f.read().split('\n'):
      if re.match(r'----|Comment:|^$',line) == None:
        pub_key_raw += bytearray(line,'utf-8')
    self.pub_key = paramiko.RSAKey(data=decodebytes(pub_key_raw))

  def check_channel_request(self, kind, chanid):
    if kind == 'session':
      return paramiko.OPEN_SUCCEEDED

  def check_auth_publickey(self, username, key):
    print(
      f"Auth attempt:\n"
      f"- Username: {username}\n"
      f"- Key fingerprint: {hexlify(key.get_fingerprint()).decode('utf-8')}"
    )
    if (username == "ABS") and (key == self.pub_key):
      print("✔ Auth successful")
      return paramiko.AUTH_SUCCESSFUL 
    print("✗ Auth failed")
    return paramiko.AUTH_FAILED

  def get_allowed_auths(self, username):
    return 'publickey'

  def check_channel_exec_request(self, channel, command):
    self.req_proc.process_external_request(command)
    self.event.set()
    return True