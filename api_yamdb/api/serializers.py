from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
import re


class ValueFromViewKeyWordArgumentsDefault:
    """Уникальный класс при вызове которого передается поле сериализатора из
    контекста которого достается нужный ключ и его значение"""
    # При вызове класса в него должно обязательно передаваться поле
    requires_context = True

    def __init__(self, context_key):
        """Сохранение полученного поля в переменную key"""
        self.key = context_key

    def __call__(self, serializer_field):
        """__call__ отвечает за вызов экземпляров этого класса"""
        return serializer_field.context.get('view').kwargs.get(self.key)

    def __repr__(self):
        """__repr__ выдает текстовое или строковое представление сущности
        или объекта"""
        return '%s()' % self.__class__.__name__


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'review', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=ValueFromViewKeyWordArgumentsDefault('title_id')
    )

    # title = serializers.SlugRelatedField(
    #     slug_field='name',
    #     default=Title.objects.all(),
    #     read_only=True
    # )

    def create(self, validated_data):
        title = get_object_or_404(Title, pk=validated_data.pop('title'))
        review = Review.objects.create(**validated_data, title=title)
        return review

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'pub_date', 'title', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Вы не можете оставить повторную рецензию',
            )
        ]


class UserSerializer(serializers.ModelSerializer):

    # def validate_username(self, username):
    #     if username.lower() == 'me':
    #         raise serializers.ValidationError(
    #             'Использовать "me" в качестве username запрещено.'
    #         )
    #
    #     result = re.findall(r'[^\w-]', username)
    #     if result:
    #         raise serializers.ValidationError(
    #             f'Не используйте {", ".join(_ for _ in result)} в username!'
    #         )
    #     return username

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


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        model = Genre
        fields = ('slug', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, obj):
        if obj.reviews.exists():
            title = obj.reviews.aggregate(rating=Avg('score'))
            return title['rating']

    class Meta:
        model = Title
        fields = ('id', 'category', 'genre', 'name', 'year', 'rating',
                  'description')
        read_only_field = ('id', 'rating')


class TitleSerializerDetail(TitleSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(read_only=True, many=True)
