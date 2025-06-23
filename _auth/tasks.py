
from celery import shared_task
from .utils import Verification

class MailService:
    @shared_task
    def send_verification_email(email,action):
        code=Verification.generateCode(email=email,action=action)
        print(f"Sending verification email to {email}:{action}:{code}")

