from rest_framework import permissions


class IsOwnerModeratorAdminOrReadOnly(permissions.BasePermission):
    message = 'Нельзя изменять или удалять чужой контент'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role in ['admin', 'moderator']
                or request.user.is_superuser)
