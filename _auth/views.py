from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Auth
from .tasks import MailService
from .utils import PasswordHash
 # Create your views here.
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
                MailService.send_verification_email.delay(email)
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
        MailService.send_verification_email.delay(email)
        return Response({"message":"Signup Successful!! Please verify your account"},status=200)



class VerifyViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"message": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":"Hello from server"},status=200)
    



class ForgetPasswordViewSet(viewsets.ViewSet):
    def create(self,request):
        
        return Response({"message":"Hello from server"},status=200)
    



class ResetPasswordViewSet(viewsets.ViewSet):
    def create(self,request):
        
        return Response({"message":"Hello from server"},status=200)