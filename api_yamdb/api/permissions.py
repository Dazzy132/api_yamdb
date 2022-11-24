from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class AuthorModeratorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Пользователи могут просматривать содержимое, но
    взаимодействовать с ним может только автор или
    модератор/администратор/суперпользователь"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ('moderator', 'admin')
            or request.user.is_superuser
        )


class IsAdminOrSuperUser(BasePermission):
    """Исключительные права на управление контентом для админа и
    суперпользователя."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """GET разрешен для всех юзеров, остальные методы только для админа и
     суперпользователя"""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_superuser
        )