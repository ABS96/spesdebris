import json
import requests
import base64


class FCMHandler:

    def __init__(self, account, secret):
        self.account = account
        self.secret = secret

    def send_message(self, device, payload):
        print("Sending cloud message")

        json_request = {
            "secret": self.secret,
            "to": self.account,
            "device": device,
            "payload": base64.urlsafe_b64encode(
                json.dumps(payload).encode()
            )
        }
        response = requests.post(
            'http://llamalab.com/automate/cloud/message', data=json_request)
        print("Message sent successfully" if response.status_code ==
              200 else f"Remote response: {response.status_code}")
