from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Review, Title
from users.permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                               IsModeratorOrReadOnly)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
        | IsModeratorOrReadOnly
        | IsAdminOrReadOnly
    ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.select_related('author', 'title')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title_id=self.get_title().pk)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
        | IsModeratorOrReadOnly
        | IsAdminOrReadOnly
    ]

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
