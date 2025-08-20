import os
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:

    def __init__(self):
        self.smtp_address = os.getenv('SMTP_ADDRESS')
        self.email = os.getenv('EMAIL')
        self.smtp_app_password = os.getenv('SMTP_APP_PASSWORD')
        self.twilio_virtual_number = os.getenv('TWILIO_VIRTUAL_NUMBER')
        self.twilio_verified_number = os.getenv('TWILIO_VERIFIED_NUMBER')
        self.client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        self.connection = smtplib.SMTP(os.getenv("SMTP_ADDRESS"))

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            body=message_body,
            to=self.twilio_verified_number
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_mails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.smtp_address, self.smtp_app_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )
