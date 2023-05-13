from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    message = "you already have account"

    def has_permission(self, request, view):
        return not request.user.is_authenticated
