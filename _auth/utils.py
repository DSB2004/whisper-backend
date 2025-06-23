import bcrypt
import redis
from whisper import settings
import secrets
from enum import Enum, unique
import json

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

@unique
class VerificationAction(Enum):
    VERIFY_EMAIL = 1
    PASSWORD_RESET = 2
    PHONE_VERIFICATION = 3
    TWO_FACTOR_AUTH = 4

class VerificationError(Enum):
    SESSION = 1
    INVALID = 2
class PasswordHash:
    @staticmethod
    def hashPassword(password):
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')  

    @staticmethod
    def checkPassword(password, dbPassword):
        password_bytes = password.encode('utf-8')
        db_password_bytes = dbPassword.encode('utf-8')
        return bcrypt.checkpw(password_bytes, db_password_bytes)
    

class Verification:
    @staticmethod
    def generateCode(email, action):
        code = secrets.token_urlsafe(6) 
        key = f"verify:{code}"
        value = json.dumps({
            "email": email,
            "action": action
        })
        redis_client.setex(key, 600, value) 
        return code

    @staticmethod
    def validateCode(email,action,code):
        key = f"verify:{code}"
        data = redis_client.get(key)

        if data is None:
            return {
                "success": False,
                "code":VerificationError.SESSION,
                "message": "Expired Session"
            }

        try:
            info = json.loads(data)
            email_ = info.get("email")
            action_ = info.get("action")
        except Exception:
            return {
                "success": False,
               "code":VerificationError.SESSION,
                "message": "Expired Session"
            }
        
        redis_client.delete(key)
        if(action!=action_):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message": "Expired Session"
            }

        if(email!=email_):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message": "Expired Session"
            }
        return {
            "success": True,
            "message": "Verification successful",
        }