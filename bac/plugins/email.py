from flask_mail import Message,Mail
from flask import current_app

mail = Mail()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender = current_app.config["MAIL_DEFAULT_SENDER"],
    )

    user = current_app.config["MAIL_USERNAME"]
    password = current_app.config["MAIL_PASSWORD"]
    print(f'Send email from {user} {password} to {to}')
    mail.send(msg)
