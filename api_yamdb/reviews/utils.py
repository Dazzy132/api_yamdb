import django_filters
from django.db import models
from rest_framework import mixins, viewsets
from reviews.models import Title


class BaseModel(models.Model):

    class Meta:
        abstract = True


class BaseModelUnique(models.Model):
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField('slug', unique=True)

    class Meta:
        abstract = True


class ListCreateDestroy(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
