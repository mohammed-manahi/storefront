from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """ Custom permission class for admin privileges """

    def has_permission(self, request, view):
        # safe methods include get, head and options
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
