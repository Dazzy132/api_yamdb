from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Genres, Categories

class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group"""

    class Meta:
        model = Genres
        fields = ('slug', 'name')
        read_only_fields = ('name', 'slug',)
