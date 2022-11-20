from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Comment, Review

User = get_user_model()


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

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     """Кастомная работа токена"""
#     username_field = User.EMAIL_FIELD
#
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['email'] = user.email
#         return token
