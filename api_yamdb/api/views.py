from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from reviews.models import Title, Genres, Categories
from api.serializers import GenreSerializer


User = get_user_model()


class GenreViewSet(viewsets.ModelViewSet):
    """Viewset для модели Post."""
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)