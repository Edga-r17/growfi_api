# from django.shortcuts import render ##

# REST Framework
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from users.backends import GrowfiUserTokenAuthentication


class RequireAuthenticationMixin(object):
    permission_classes = (IsAuthenticated,)


class RequireUserTokenMixin(RequireAuthenticationMixin):
    authentication_classes = (GrowfiUserTokenAuthentication,)
    

class RetrieveUpdateDeleteGeneralMixin(object):
    """
    This Mixin mage the base operations in RUD Views
        1. Manage partial updates
        2. Manage log updates/deletes actions and logic delete filters.
    """
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 250
    page_size_query_param = 'page_size'
    max_page_size = 500


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 150
    page_size_query_param = 'page_size'
    max_page_size = 250


class IsOwnerOrAdmin(permissions.IsAuthenticated, permissions.BasePermission):
    """Check permission to read or modify profile."""

    def has_object_permission(self, request, view, obj):
        """Check permissions method."""
        user = request.user

        if obj == user or (user.is_admin or user.is_staff):
            return True

        return False
