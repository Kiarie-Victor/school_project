from django.core.mail import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()

def sendEmail(reg_no, otp_code, email) -> bool:
    receiver = email
    subject = f'Otp Verification {otp_code}'
    sender = os.getenv('EMAIL_HOST_USER')
    message = f"Dear {reg_no}, \n Your code is: {otp_code}. \n Use it to access your account. If you didn't request this, simply ignore this message."

    try:
        email = EmailMessage(subject=subject, body=message,
                             from_email=sender, to=[receiver])
        email.send(fail_silently=False)
        return True
    except Exception as e:
        return False
