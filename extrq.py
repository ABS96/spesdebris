# Script by ABS
# Personal keys included, must remove before releasing to the public
#
# Run the following commands in your terminal for required dependencies:
# pip install dropbox
# pip install pyperclip

from subprocess import check_output, CalledProcessError
from dbxhandler import DropboxHandler
import pyperclip
from base64 import decodebytes
import configparser
from fcmhandler import FCMHandler

config = configparser.ConfigParser()
config.read('settings.ini')

dbh = DropboxHandler(config.get('APIkeys','Dropbox'))
fcmh = FCMHandler(config.get('Client','Account'),config.get('APIkeys','Automate'))

payload = {
  "command": "Notification action",
  "action": 1,
  "id": 7
}
fcmh.send_message(config.get('Client','Device'),payload)

def process_external_request(rq):
  commands = {
    'echo': print,
    'setpwr': set_power,
    'setvol': set_volume,
    'setclip': set_clipboard,
    'getfile': dbh.get_file,
    'mirnot': mirror_notification
  }

  #print("]",rq)
  drq = decodebytes(rq).decode('utf-8')
  request = drq.split(" ", 1)
  print(">", drq)

  try:
    commands[request[0]](request[1])
  except KeyError:
    print("Error: that's not a valid command")
    return
  except IndexError:
    print("Error: the command has no arguments")
    return
  except CalledProcessError as e:
    print("Command '{}' returned with error code {}".format(e.cmd, e.returncode))

def set_power(power_state):
  psc = {
    'sleep': 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0',
    'off': 'shutdown /s',
    'reboot': 'shutdown /r'
  }
  check_output(psc[power_state], shell=True) #.decode()

def set_volume(s):
  if s == "mute" or s == "unmute":
    check_output("nircmdc mutesysvolume {}".format("1" if s == "mute" else "0"), shell=True)
  else:
    pass
  # TODO: set volume
    
def set_clipboard(s):
  pyperclip.copy(s.replace("\n","\r\n"))

def mirror_notification(s):
  print("Mirroring notification:",s)