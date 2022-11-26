from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SelfUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """Валидация всех полей. Если вызвать проверку только для кода, то
        могут проскочить незаполненные username, что приведет к ошибкам"""
        user = get_object_or_404(User, username=data.get('username'))
        confirmation_code = data.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {"detail": "Введен неправильный код"}
            )
        return data

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )
