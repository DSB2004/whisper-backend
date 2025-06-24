from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User,IndustryType
from .serializer import UserSerializer
from .tasks import UpdateProfilePic
from django.db import IntegrityError
class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def partial_update(self, request):
        email=request.emails
        
        description=request.data.get("description")
        industryType = request.data.get("industryType")

        if not description or not industryType:
            return Response({"message": "description and industryType required"}, status=status.HTTP_400_BAD_REQUEST)
        if(industryType not in IndustryType):
            return Response({"message":"industryType invalid"},status=status.HTTP_409_CONFLICT)
        try:    
            user=User.objects.get(email=email)
            user.description=description
            user.industryType=industryType

        except User.DoesNotExist:
            return Response({"message":"User not found"},status=400)

        return Response({"message": f"User updated"})
    
    def retrieve(self, request):
        try:    
            email=request.email
            user=User.objects.get(email=email)
            return Response({"message":"User found","user":user},status=200)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=400)
    
    @action(detail=False, methods=['patch'], url_path='update-username')
    def updateUsername(self, request):
        try:    
            email=request.email
            username=request.data.username
            user=User.objects.get(email=email)

            user.username=username

        except User.DoesNotExist:
            return Response({"message":"User not found"},status=400)
        except IntegrityError:
            return Response({"message":"Username already in use"},status=400)


    @action(detail=False, methods=['patch'], url_path='update-profile-pic')
    def updateProfilePic(self, request):

        try:    
            email=request.email
            profile_pic = request.FILES.get('profile_pic')
            User.objects.get(email=email)
            
            if not profile_pic:
                return Response({'error': 'No profile picture uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
            UpdateProfilePic.updateProfilePic.delay(email=email,file=profile_pic)
            return Response({'message': 'Profile picture will be updated soon.'}, status=status.HTTP_202_ACCEPTED)

        except User.DoesNotExist:
            return Response({"message":"User not found"},status=400)
        
