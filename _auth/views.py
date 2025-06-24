from rest_framework import viewsets,status
from rest_framework.response import Response

from .models import Auth
from .tasks import MailService
from .utils import PasswordHash,TokenType,TokenError,JWT,VerificationAction,Verification



class LoginViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"message": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            auth=Auth.objects.get(email=email)
            if(PasswordHash.checkPassword(password=password,dbPassword=auth.password)==False):
                return Response({"message":"Incorrect Password"},status=400)
            if(auth.isVerified==False):
                MailService.send_verification_email.delay(email,VerificationAction.VERIFY_EMAIL)
                return Response({"message":"Please verify your account"},status=403)
        except Auth.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)


        return Response({"message":"Hello from server"},status=200)
    


class SignUpViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"message": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            auth=Auth.objects.get(email=email)
            if(auth):
                return Response({"message":"User already exist"},status=400)
        except Auth.DoesNotExist:
            pass
        
        hashPassword=PasswordHash.hashPassword(password=password)
        Auth.objects.create(email=email,password=hashPassword)
        MailService.sendVerificationEmail.delay(email,VerificationAction.VERIFY_EMAIL)
        return Response({"message":"Signup Successful!! Please verify your account"},status=200)



class VerifyViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        action = request.data.get('action')
        code = request.data.get('code')


        if not email or not action or not code:
            return Response({"message": "email, code and action  required"}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            auth=Auth.objects.get(email=email)
            status=Verification.validateCode(email,action,code)
            if(status["success"]==False):
                return Response({"message": "required"}, status=status.HTTP_400_BAD_REQUEST)
            
            auth.isVerified=True
            auth.save()
        except Auth.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        
        accessTokenData={
            "email":email,
            "type":TokenType.ACCESS
        }   
        refreshTokenData={
            "email":email,
            "type":TokenType.REFRESH
        }    
        
        accessToken_=JWT.generateToken(accessTokenData,3600*24) # 1 day
        refreshToken_=JWT.generateToken(refreshTokenData,7*24*3600) # 7 days
        return Response({"message":"Your account has beed verified", "accessToken":accessToken_,"refreshToken":refreshToken_},status=200)
    



class ForgetPasswordViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        
        if not email:
            return Response({"message": "email required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Auth.objects.get(email=email)
            MailService.sendVerificationEmail.delay(email,VerificationAction.PASSWORD_RESET)
        except Auth.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        

        return Response({"message":f"Password reset email has been sent to {email}"},status=200)
    



class ResetPasswordViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        action = request.data.get('action')
        code = request.data.get('code')
        password=request.data.get('password')

        if not email or not action or not code or not password:
            return Response({"message": "email, code, password and action  required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            auth=Auth.objects.get(email=email)
            hashPassword=PasswordHash.hashPassword(password=password)
            auth.password=hashPassword
            auth.save()
        except Auth.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        
        return Response({"message":"Password reset"},status=200)