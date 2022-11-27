from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user

        return False
