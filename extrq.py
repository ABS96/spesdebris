from base64 import decodebytes
import json
from subprocess import call, CalledProcessError
from time import sleep
import webbrowser

import pyperclip
from win10toast import ToastNotifier
# from win32gui import Shell_NotifyIcon, NIM_DELETE


class RequestProcessor():
    """
    This class processes all the requests received from
    your Android device.
    """

    def __init__(self, DropboxHandler, FCMHandler):
        self.dbh = DropboxHandler
        self.fcmh = FCMHandler
        self.toaster = ToastNotifier()

    def process_external_request(self, raw_payload):
        """
        This method decodes the incoming base64 and JSON encoded payload
        and executes the requested command
        """

        commands = {
            'disnot': self.dismiss_notification,
            'echo': self.echo,
            'getfile': self.get_file,
            'mirnot': self.mirror_notification,
            'openlink': self.open_link,
            'setclip': self.set_clipboard,
            'setpwr': self.set_power,
            'setvol': self.set_volume,
        }

        decoded_payload = decodebytes(raw_payload).decode('utf-8')
        print(">", decoded_payload)
        request = json.loads(decoded_payload)

        try:
            commands[request["command"]](request)
        except KeyError:
            print(f"Error: {request['command']} is not a valid command")
        except CalledProcessError as e:
            print(f"Info: Command '{e.cmd}' "
                  f"returned with error code {e.returncode}")

    def echo(self, cmdin):
        txt = cmdin["text"]
        print(txt)

    def set_power(self, cmdin):
        power_state = cmdin["powerstate"]
        psc = {
            'sleep': 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0',
            'off': 'shutdown /s',
            'reboot': 'shutdown /r'
        }
        call(psc[power_state], shell=True)

    def set_volume(self, cmdin):
        s = cmdin["volume"]
        if s == "mute" or s == "unmute":
            call(
                f"nircmdc mutesysvolume {'1' if s == 'mute' else '0'}",
                shell=True
            )

    def set_clipboard(self, cmdin):
        s = cmdin["text"]
        pyperclip.copy(
            s.replace("\n", "\r\n")
        )

    def mirror_notification(self, cmdin):
        self.toaster.show_toast(
            title=cmdin["title"],
            msg=cmdin["message"],
            duration=10,
            threaded=True
        )

    def dismiss_notification(self, cmdin):
        # TODO
        print("destroy", cmdin["id"])
        # Shell_NotifyIcon(NIM_DELETE, (self.toaster.hwnd, 0))

    def get_file(self, cmdin):
        # Dropbox needs a little time to register the new file ¯\_(ツ)_/¯
        sleep(3)
        self.dbh.download_file(remote_path=cmdin["pathFrom"])

    def open_link(self, cmdin):
        webbrowser.open(url=cmdin["link"])
