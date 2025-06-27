from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User,IndustryType
from .serializer import UserSerializer
from .tasks import UpdateProfilePic
from django.db import IntegrityError

class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    def get_user(self, request):
        email = getattr(request, "email", None)
        if not email:
            return None, Response({"message": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            return user, None
        except User.DoesNotExist:
            return None, Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request):
        user, error = self.get_user(request)
        if error:
            return error

        description = request.data.get("description")
        industry_type = request.data.get("industryType")

        if not description or not industry_type:
            return Response({"message": "description and industryType required"}, status=status.HTTP_400_BAD_REQUEST)

        if industry_type not in IndustryType.values:
            return Response({"message": "industryType invalid"}, status=status.HTTP_409_CONFLICT)

        serializer = self.serializer_class(user, data={
            "description": description,
            "industryType": industry_type
        }, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated", "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        user, error = self.get_user(request)
        if error:
            return error
        serializer = self.serializer_class(user)
        return Response({"message": "User found", "user": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='update-username')
    def updateUsername(self, request):
        user, error = self.get_user(request)
        if error:
            return error

        username = request.data.get("username")
        if not username:
            return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        user.username = username
        try:
            user.save()
            return Response({"message": "Username updated"})
        except IntegrityError:
            return Response({"message": "Username already in use"}, status=status.HTTP_409_CONFLICT)

    @action(detail=False, methods=['patch'], url_path='update-profile-pic')
    def updateProfilePic(self, request):
        user, error = self.get_user(request)
        if error:
            return error

        profile_pic = request.FILES.get('profile_pic')
        if not profile_pic:
            return Response({'error': 'No profile picture uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        UpdateProfilePic.updateProfilePic.delay(email=user.email, file=profile_pic.name)
        return Response({'message': 'Profile picture will be updated soon.'}, status=status.HTTP_202_ACCEPTED)
