import bcrypt
import redis
from whisper import settings
import secrets
from enum import Enum, unique
import json
import jwt
import datetime


redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

@unique
class VerificationAction(Enum):
    VERIFY_EMAIL = 1
    PASSWORD_RESET = 2
    PHONE_VERIFICATION = 3
    TWO_FACTOR_AUTH = 4


@unique
class VerificationError(Enum):
    SESSION = 1
    INVALID = 2


@unique
class TokenError(Enum):
    EXPIRED = 1
    INVALID = 2

@unique
class TokenType(Enum):
    ACCESS = 1
    REFRESH = 2





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
        
        
        if(action!=action_):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message": "Invalid Action"
            }

        if(email!=email_):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message": "Invalid Action"
            }
            
        redis_client.delete(key)
        
        return {
            "success": True,
            "message": "Verification successful",
        }
    


class JWT:
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    @staticmethod
    def generateToken(payload, expires_in):
        payload_copy = payload.copy()
        payload_copy['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        return jwt.encode(payload_copy, JWT.SECRET_KEY, algorithm=JWT.ALGORITHM)

    @staticmethod
    def decodeToken(token):
        try:
            token = token.split(' ')[1]  # Bearer <token>
            decoded = jwt.decode(token, JWT.SECRET_KEY, algorithms=[JWT.ALGORITHM])
            return {"success": True, "data": decoded}
        except jwt.ExpiredSignatureError:
            return {"success": False, "message": "Token has expired", "code": TokenError.EXPIRED}
        except jwt.InvalidTokenError:
            return {"success": False, "message": "Invalid token", "code": TokenError.INVALID}

    @staticmethod
    def refreshTokens(refreshToken):
        token = JWT.decodeToken(refreshToken)

        if not token["success"]:
            return token
        if token["data"]["type"] != TokenType.REFRESH:
            return {"success": False, "message": "Invalid token", "code": TokenError.INVALID}

        userData = token["data"]

        accessTokenData = {
            "email": userData["email"],
            "type": TokenType.ACCESS
        }
        refreshTokenData = {
            "email": userData["email"],
            "type": TokenType.REFRESH
        }

        accessToken_ = JWT.generateToken(accessTokenData, 3600 * 24)
        refreshToken_ = JWT.generateToken(refreshTokenData, 7 * 24 * 3600)

        return {"success": True, "accessToken": accessToken_, "refreshToken": refreshToken_}
