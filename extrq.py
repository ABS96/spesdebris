from base64 import decodebytes
from dbxhandler import DropboxHandler
from fcmhandler import FCMHandler
from subprocess import check_output, CalledProcessError
import configparser
import pyperclip

class RequestProcessor():

  def __init__(self, dropboxApiKey, FCMAccount, FCMSecret):
    self.dbh = DropboxHandler(dropboxApiKey)
    self.fcmh = FCMHandler(FCMAccount,FCMSecret)

  def process_external_request(self, rq):
    commands = {
      'echo': print,
      'setpwr': self.set_power,
      'setvol': self.set_volume,
      'setclip': self.set_clipboard,
      'getfile': self.dbh.get_file,
      'mirnot': self.mirror_notification
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

  def set_power(self, power_state):
    psc = {
      'sleep': 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0',
      'off': 'shutdown /s',
      'reboot': 'shutdown /r'
    }
    check_output(psc[power_state], shell=True) #.decode()

  def set_volume(self, s):
    if s == "mute" or s == "unmute":
      check_output("nircmdc mutesysvolume {}".format("1" if s == "mute" else "0"), shell=True)
    else:
      pass
    # TODO: set volume
      
  def set_clipboard(self, s):
    pyperclip.copy(s.replace("\n","\r\n"))

  def mirror_notification(self, s):
    print("Mirroring notification:",s)