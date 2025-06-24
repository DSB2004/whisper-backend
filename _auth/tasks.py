
from celery import shared_task
from .utils import Verification
import logging

logger = logging.getLogger('whisper')

class MailService:
    @shared_task
    def sendVerificationEmail(email,action):
        try:
            code=Verification.generateCode(email=email,action=action)
            logger.info(f"Sending verification email to {email}:{action}:{code}")
        except Exception as e:
            logger.error(f"[SEND VERIFICATION EMAIL] Failed to send email {e}")
