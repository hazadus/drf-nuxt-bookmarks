from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit/delete it.

    Reference: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
    """

    def has_object_permission(self, request, view, obj):
        """
        Any actions are only allowed to the owner.
        """
        return obj.user == request.user
