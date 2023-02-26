from twilio.rest import Client
import os
from dotenv import load_dotenv
import smtplib
# TODO: handle the not valid email address error (SMTPRecipientsRefused(senderrs)). occurs when there is no @ sign
load_dotenv(".env")

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = os.environ["TWILIO_PHONE_NUMBER"]
client = Client(account_sid, auth_token)
sender_email = os.environ["SENDER_EMAIL"]
email_password = os.environ["EMAIL_PASSWORD"]


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, structured_flight_data: dict):
        self.data = structured_flight_data

    def send_sms_notification(self):
        message = client.messages.create(to="+16204408116",
                                         from_=twilio_phone_number,
                                         body=f"\nLow price alert! Only {self.data['price']} to fly from "
                                              f"{self.data['depart_city']}-{self.data['depart_code']} to "
                                              f"{self.data['arrival_city']}-{self.data['arrival_code']}, from "
                                              f"{self.data['utc_leave_date']} to {self.data['utc_return_date']} \n"
                                              f"{self.data['link_to_book']}")
        print(message.status)

    def send_email_notification(self, email: str):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=sender_email, password=email_password)
            connection.sendmail(from_addr=sender_email,
                                to_addrs=f"{email}",
                                msg=f"Subject: Low price alert!\n\nOnly {self.data['price']} "
                                    f"to fly from "
                                    f"{self.data['depart_city']}-{self.data['depart_code']} to "
                                    f"{self.data['arrival_city']}-{self.data['arrival_code']}, from "
                                    f"{self.data['utc_leave_date']} to {self.data['utc_return_date']} \n"
                                    f"{self.data['link_to_book']}")
