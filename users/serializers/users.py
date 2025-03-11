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

class UserDetailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='growfi_auth_token.key', read_only=True)

    class Meta:
        model = GrowfiUser
        fields = ('id', 'name', 'email', 'phone', 'photo', 'initials', 'token')