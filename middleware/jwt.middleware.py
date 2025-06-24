import logging
from rest_framework.response import Response
from _auth.utils import TokenError,JWT,TokenType
from fnmatch import fnmatch
from whisper.settings import SKIP_VERIFICATION



logger = logging.getLogger('whisper')



class JWTMiddleware:
    def skip(method, path):
        for allowed_method, pattern in SKIP_VERIFICATION:
            if (allowed_method == "*" or method.upper() == allowed_method.upper()) and fnmatch(path, pattern):
                return True
        return False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if(self.skip(request.method,request.path)):
            response = self.get_response(request)
            return response
        
        token = request.headers.get('Authorization')
        if(not token):
            return Response({"message":"Access token not given"},status=403)

        decoded=JWT.decodeToken(token=token);

        if(decoded["success"] is False):
            if(decoded['code']==TokenError.INVALID):
                return Response({"message":"Access token is not valid"},status=403)
            if(decoded['code']==TokenError.EXPIRED):
                return Response({"message":"Access token has expired"},status=401)
        
        if token["data"]["type"] != TokenType.ACCESS:
            return Response({"message":"Access token is not valid"},status=403)

        request.email = decoded["data"]["email"]
        response = self.get_response(request)
        return response
        