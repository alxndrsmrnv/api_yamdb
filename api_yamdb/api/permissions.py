from rest_framework import permissions


class IsOwnerModeratorAdminOrReadOnly(permissions.BasePermission):
    message = 'Нельзя изменять или удалять чужой контент'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin()
                or request.user.is_moderator()
                or request.user.is_superuser)


class IsRoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.is_admin()
                or request.user.is_superuser)


class IsRoleAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        role = (obj.username == request.user.username)
        role = role or request.user.is_admin()
        return role


class AdminOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin()
                         or request.user.is_superuser)))
