from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models.users import GrowfiUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowfiUser
        fields = '__all__'

class UserDetailTokensSerializer(serializers.ModelSerializer):
    """
    """
    
    class Meta:
        model = GrowfiUser
        fields = (
            'id', 'password', 'name', 'surname',
            'email'
        )