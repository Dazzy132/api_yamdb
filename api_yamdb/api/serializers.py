from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Comment, Review, Title, Genres, Categories

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group"""

    class Meta:
        model = Genres
        fields = ('slug', 'name')
        read_only_fields = ('name', 'slug',)
        

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date', 'review', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date', 'title', 'author')


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


# ------------------------------- TEST ----------------------------------------


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title


# ------------------------------- TEST ----------------------------------------
