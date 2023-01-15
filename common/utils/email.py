import sendgrid
from sendgrid.helpers.mail import Mail
from decouple import config

def send_email(to, subject, content, sender='alfcomputacion@gmail.com'):
    sg = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
    mail = Mail(
        from_email=sender,
        to_emails=to,
        subject=subject,
        html_content=content
    )

    return sg.send(mail)