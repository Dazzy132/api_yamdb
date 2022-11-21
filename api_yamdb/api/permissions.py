from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS


class AuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Пользователи могут просматривать содержимое, но
    взаимодействовать с ним может только автор или
    модератор/администратор/суперпользователь"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role in ('moderator', 'admin')
                or request.user.is_superuser)


class IsAdminOrSuperUser(BasePermission):
    """Полные права на управление всем контентом для админа и суперюзера."""

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
