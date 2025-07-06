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
            'bio',
            'industryType',
            'profilePic',
            'DOB',
            'ethnicGroup',
            'preferredTopic',
            'preferredLanguage',
            'country',
            'gender',
            'createdAt'
        ]
        read_only_fields = ['id', 'flagCount', 'isBanned', 'createdAt', 'updateAt', 'bannedAt']
