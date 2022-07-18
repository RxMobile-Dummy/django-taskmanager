"""Email Manager for this app"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from multiprocessing import AuthenticationError
import smtplib
from jinja2 import Environment

from projects.models import ProjectAssigneeModel  # Jinja2 templating

CHARSET = "UTF-8"

PORT = 25
PASSWORD = "Radixweb@13"
SMTP_SERVER = "192.168.100.101"
SENDER_EMAIL = "anirudh.chawla@radixweb.com"


class EmailManager:
    """Class for managing email"""
    server = smtplib.SMTP(SMTP_SERVER, PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()

    def __init__(self) -> None:
        try:
            self.server.login(SENDER_EMAIL, PASSWORD)
        except Exception as exception:
            logging.debug(exception)

    def send_email(self, recipient, subject, project_id, assignee_id,template):
        """Function for sending email"""
        try:
            body = MIMEText(
                Environment().from_string(template).render(
                    title='Hello World!'
                ), "html"
            )
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            # body = MIMEText(content,"html")
            message.attach(body)
            self.server.sendmail(SENDER_EMAIL, recipient, message.as_string())
            return {
                "message": "Email has been sent successfully on your email address",
                "status": True
            }
        except Exception as exception:
            print(exception)
            return {
                "message": "Error while sending an email",
                "status": False
            }

    def forgot_password(self, recipient, subject,template):
        """Function for sending otp on email if user forgets password"""
        try:
            body = MIMEText(
                Environment().from_string(template).render(
                    title='Hello World!'
                ), "html"
            )
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            # body = MIMEText(content,"html")
            message.attach(body)
            self.server.sendmail(SENDER_EMAIL, recipient, message.as_string())
            return {
                "message": "OTP has been sent successfully on your email address",
                "status": True
            }
        except Exception as exception:
            print(exception)
            return {
                "message": "Error while sending an email",
                "status": False
            }
