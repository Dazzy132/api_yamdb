from api.permissions import AuthorModeratorOrReadOnly, IsAdminOrReadOnly

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerDetail)
from .utils import ListCreateDestroy, TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.select_related('author', 'title')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title_id=self.get_title().pk)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title_id=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_review().comments.select_related('author', 'review')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.get_review().pk
        )


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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'id'
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

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
