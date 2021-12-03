import os
from twilio.rest import Client
class Notification:

    def send_text(self, message, to):
        twilio_sid = os.getenv('TWILIO_SID')
        twilio_token = os.getenv('TWILIO_TOKEN')
        client = Client(twilio_sid, twilio_token)
        message_info = client.messages.create(body=message, from_='+13155644341', to=f'+1{to}')
        return message_info.sid