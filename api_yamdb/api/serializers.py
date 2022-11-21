from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Comment, Review, Title, Genres, Category
from users.models import User

from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genres"""

    class Meta:
        model = Genres
        fields = ('slug', 'name')
        

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
                'Использовать \'me\' в качестве username запрещено'
            )
        return username

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


