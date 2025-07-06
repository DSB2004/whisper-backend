from django.shortcuts import render
from rest_framework import viewsets,status
# Create your views here.
class PostViewSet(viewsets.ViewSet):
    def create(self,request): 
        email = request.email
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
        pass
