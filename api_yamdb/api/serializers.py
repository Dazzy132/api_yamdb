from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Categories, Comment, Genres, Review, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group"""

    class Meta:
        model = Genres
        fields = ('slug', 'name')
        read_only_fields = ('name', 'slug',)


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     'username', slug_field='username', read_only=True
    # )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date', 'review', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     'username', slug_field='username', read_only=True
    # )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date', 'title')


class UserSerializer(serializers.ModelSerializer):

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать "me" в качестве username запрещено.'
            )
        return username

    class Meta:
        model = User
        exclude = ['id']


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()
    username = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
