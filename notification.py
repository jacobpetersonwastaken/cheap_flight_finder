import os
from twilio.rest import Client
from dotenv import load_dotenv
class Notification:


    def send_text(self, message, to):
        """Sends text message using Twilio"""
        twilio_sid = os.getenv('TWILIO_SID')
        twilio_token = os.getenv('TWILIO_TOKEN')
        client = Client(twilio_sid, twilio_token)
        message_info = client.messages.create(body=message, from_=os.getenv('TWILIOPHONE'), to=f'+1{to}')
        return message_info.sid