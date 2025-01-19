from rest_framework import permissions



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return obj == request.user


class IsVerified(permissions.BasePermission):
    """
    Custom permission to only allow verified users to access the API.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return request.user.is_verified


class IsNotVerified(permissions.BasePermission):
    """
    Custom permission to only allow verified users to access the API.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return not request.user.is_verified


class IsOwnObj(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return obj.user == request.user


