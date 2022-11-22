from rest_framework import serializers

from reviews.models import Comment, Genres, Review
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genres"""

    class Meta:
        model = Genres
        fields = ('slug', 'name')
        read_only_fields = (
            'name',
            'slug',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date', 'review', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date', 'title', 'author')


class UserSerializer(serializers.ModelSerializer):

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать "me" в качестве username запрещено.'
            )
        return username

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
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )
