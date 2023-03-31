from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from users.permissions import IsAdminOrReadOnly

from .models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitleSerializerDetail)
from .utils import ListCreateDestroy, TitleFilter


class GenreViewSet(ListCreateDestroy):
    """Viewset для модели Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для модели Title"""
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        return (
            Title.objects
            .annotate(rating=Avg('reviews__score'))
            .select_related('category')
            .prefetch_related('genre')
            .order_by('-pub_date')
        )

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleSerializerDetail
        return TitleSerializer


class CategoryViewSet(ListCreateDestroy):
    """Viewset для модели Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
