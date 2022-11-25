from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Comment, Review, Title


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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к рецензиям"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'review', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для рецензий на произведения"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=ValueFromViewKeyWordArgumentsDefault('title_id')
    )

    def create(self, validated_data):
        title = get_object_or_404(Title, pk=validated_data.pop('title'))
        review = Review.objects.create(**validated_data, title=title)
        return review

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'pub_date', 'title', 'author')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Вы не можете оставить повторную рецензию',
            )
        ]
