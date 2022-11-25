from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class IsAuthorOrAuthReadOnly(IsAuthenticatedOrReadOnly):
    """Пользователи могут просматривать содержимое, но
    взаимодействовать с ним может только автор"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
        )


class IsModeratorOrAuthReadOnly(IsAuthenticatedOrReadOnly):
    """Кто угодно может просматривать содержимое, но
    взаимодействовать с ним может только модератор"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_superuser
        )


class IsAdminOrAuthReadOnly(IsAuthenticatedOrReadOnly):
    """Кто угодно может просматривать содержимое, но
    взаимодействовать с ним может только админ"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """GET разрешен для всех юзеров, остальные методы только для админа и
     суперпользователя"""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrSuperUser(BasePermission):
    """Исключительные права на управление контентом для админа и
    суперпользователя."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )
