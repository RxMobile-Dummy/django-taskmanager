from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib,ssl
from jinja2 import Environment        # Jinja2 templating

CHARSET = "UTF-8"


port  = 25
password = "Radixweb@13"
smtp_server = "192.168.100.101"
SENDER_EMAIL="anirudh.chawla@radixweb.com"

class EmailManager:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo()
    server.starttls()
    server.ehlo()

    def __init__(self) -> None:
        try:
            self.server.login(SENDER_EMAIL,password)
        except Exception as e:
            logging.debug(e)
    
    def sendEmail(self,recepient,subject,content,project_id,assignee_id):
        TEMPLATE = '''
<!DOCTYPE html>
<html>
<body>

<h1>Verification to assign project</h1>

<p>Click on verify button to get access of the project you have been assigned</p>


<form action="http://127.0.0.1:8000/taskapp/index/{0}/{1}/" method="post">

    <input type="submit" value="Verify" />
</form>
<p id="demo"></p>
</body>
</html>
'''.format(project_id,assignee_id)
        try:
            body = MIMEText(
    Environment().from_string(TEMPLATE).render(
        title='Hello World!'
    ), "html"
)
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = recepient
            # body = MIMEText(content,"html")
            message.attach(body)
            self.server.sendmail(SENDER_EMAIL,recepient,message.as_string())
            return {
                "message":"Email has been sent successfully on your email address",
                "status":True
            }
        except Exception as e:
            print(e)
            return {
                "message":"Error while sending an email",
                "status":False
            }


