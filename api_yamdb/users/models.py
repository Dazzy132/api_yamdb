from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from .validators import validate_username
from dataclasses import dataclass
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Введите адрес своей электронной почты')
        if not username:
            raise ValueError('Введите username')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        if extra_fields.get('role') in (User.UserRole.ADMIN,
                                        User.UserRole.MODERATOR):
            extra_fields.update({'is_staff': True})
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', User.UserRole.USER)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.UserRole.ADMIN)
        if extra_fields.get('role') != User.UserRole.ADMIN:
            raise ValueError('Суперпользователь должен быть с группой админа!')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, username, password, **extra_fields)


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

    objects = CustomUserManager()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
        if self.role in (self.UserRole.MODERATOR, self.UserRole.ADMIN):
            self.is_staff = True
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR
