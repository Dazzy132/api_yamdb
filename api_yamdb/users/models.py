from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_username
from dataclasses import dataclass


class User(AbstractUser):

    @dataclass
    class UserRole:
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    USER_ROLES = (
        (UserRole.USER, 'Аутентифицированный пользователь'),
        (UserRole.MODERATOR, 'Модератор'),
        (UserRole.ADMIN, 'Администратор'),
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[validate_username],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Пользовательская роль',
        choices=USER_ROLES,
        default='user',
        max_length=30,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR
