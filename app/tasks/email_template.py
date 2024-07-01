from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def send_email(email_to: EmailStr):
    msg = EmailMessage()
    msg['Subject'] = "Registration successful"
    msg['From'] = settings.SMTP_USER
    msg['To'] = email_to
    msg.set_content(
        f"""
        <h1>Registration successful</h1>
        User with email: {email_to} has been registered
        """,
        subtype='html'
    )
    return msg
