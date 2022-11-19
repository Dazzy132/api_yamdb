"""
В файле проведена регистрация роутера и JWT-токена для API V1.

Зарегистрированы пути для базовых моделей Post, Group, Follow, Comment.

"""


from django.urls import include, path
from rest_framework import routers

from api.views import GenreViewSet

app_name = 'djoser'

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]

router_v1 = routers.DefaultRouter()
router_v1.register(r'v1/genres', GenreViewSet)
