from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    """Другие пользователи могут просматривать детально содержимое, но
    не могут взаимодействовать с ним. Взаимодействовать может автор или
    модератор/администратор/суперпользователь"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or obj.author == request.user
                or request.user.role in ['moderator', 'admin']
                or request.user.is_superuser)


class IsAdminOrSuperUser(BasePermission):
    """Основной контент могут просматривать только администратор или
    суперпользователь. """

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin'
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user == obj
                or request.user.role == 'admin'
                or request.user.is_superuser)


class IsUserProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user == obj
                or request.user.role == 'admin' or request.user.is_superuser)
