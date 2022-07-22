"""Email Manager for this app"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from multiprocessing import AuthenticationError
import smtplib
from jinja2 import Environment

from email.message import EmailMessage
from projects.models import ProjectAssigneeModel  # Jinja2 templating

CHARSET = "UTF-8"
SENDER_EMAIL = "anirudh.chawla@radixweb.com"

class EmailManager:
    """Class for managing email"""

    def send_email(self, recipient, subject, project_id, assignee_id,template):
        """Function for sending email"""
        try:
            message = EmailMessage()
            message.add_alternative(Environment().from_string(template).render(
                    title='Hello World!'
                ))
            # message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            s = smtplib.SMTP('localhost')
            s.send_message(message)
            s.quit()

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
            message = EmailMessage()
            message.add_alternative(Environment().from_string(template).render(
                    title='Hello World!'
                ))
            # message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            s = smtplib.SMTP('localhost')
            s.send_message(message)
            s.quit()
            # body = MIMEText(content,"html")
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
