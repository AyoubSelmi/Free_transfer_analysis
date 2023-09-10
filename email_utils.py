from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__),".env")) # load env vars from .env file

email_address = os.getenv("email_address") # get email_address env var
email_password = os.getenv("email_password") # email_password env var


def send_mail(to:str, subject:str, body:str) -> None:
    """
    send email using smtp
    """
    # prepare the mail subject, sender and receiver
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = email_address
    message['To'] = to
    
    # prepare the mail body
    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = smtplib.SMTP('localhost') # start the smtp server
    server.login(email_address, email_password) # login using the credentials
    server.sendmail(email_address, to, msg_body) # send email
    server.quit() # quit the smtp server