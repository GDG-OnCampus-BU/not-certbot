import os
import sys
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

def render_certificate(email):
    with open("certificate_template.html") as file:
        template = Template(file.read())
    certificate = template.render(email=email, date=date)
    return certificate

def send_email(email, certificate):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Your Certificate"

    text = MIMEText(certificate, "html")
    msg.attach(text)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())

if __name__ == "__main__":
    email = sys.argv[1]
    name = sys.argv[2]
    commit_hash = sys.argv[3]
    certificate = render_certificate(name=name, hash=commit_hash)
    send_email(email, certificate)
