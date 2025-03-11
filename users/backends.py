from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.backends import ModelBackend

from users.models import GrowfiUser, GrowfiUserToken

from django.shortcuts import get_object_or_404


class GrowfiUserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token.split() if token else None
        keyword = 'token'

        if not token\
           or len(token) is 1 or len(token) > 2\
           or token[0].lower() != keyword:
            return None

        try:
            growfi_user_token = GrowfiUserToken.objects.get(key=token[1])
        except GrowfiUserToken.DoesNotExist:
            return None

        return (growfi_user_token.growfi_user, 'GrowfiUser')



class GrowfiUserBackend(ModelBackend):
    """
    Authenticates agains nurses.NurseUser
    This user class is based on default Django User System
    so we can use all has_perms and all perms related functions
    of default ModelBackend and only replace what we need.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        growfi_user = get_object_or_404(GrowfiUser, email=username)

        if not growfi_user or not growfi_user.check_password(password):
            return None

        return growfi_user

    def get_user(self, user_pk):
        """Returns find_user based on their Pk"""
        return get_object_or_404(GrowfiUser, pk=user_pk)
