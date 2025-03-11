from rest_framework import serializers, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from users.models.users import GrowfiUser
from django.shortcuts import get_object_or_404
from _base.views import RequireUserTokenMixin
from users.serializers.users import UserSerializer, UserDetailTokensSerializer



class UserCreateView(APIView):
    """
    Permite la creación de un nuevo usuario.
    No requiere autenticación.
    """
    def post(self, request):
        user_serializer = UserDetailTokensSerializer(data=request.data)
        if user_serializer.is_valid():
            
            user = user_serializer.save()

            token_data = {
                'user_token': user.growfi_auth_token.key
            }
            user_data = {
                'id': user.id,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'is_admin' : user.is_admin,
                'initials' : user.initials
                
            }

            response_data = {
                **user_data,
                **token_data,
            }
            print("Response Data:", response_data)
            

            return Response(response_data)
        else:
            return Response(user_serializer.errors)


class UserProfileView(generics.RetrieveUpdateAPIView, RequireUserTokenMixin):
    """
    Permite a un usuario obtener y actualizar su perfil.
    Solo accesible para usuarios autenticados.
    """
    queryset = GrowfiUser.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
