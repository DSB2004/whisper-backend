from rest_framework import serializers
from .models import User, IndustryType

class UserSerializer(serializers.ModelSerializer):
    industryType = serializers.ChoiceField(choices=IndustryType.choices, default=IndustryType.OTHER)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'description',
            'industryType',
            'profilePic',
            'DOB',
            'isBanned',
            'createdAt'
        ]
        read_only_fields = ['id', 'flagCount', 'isBanned', 'createdAt', 'updateAt', 'bannedAt']
