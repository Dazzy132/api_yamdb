from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserAuthViewSet,
                    UserProfileViewSet, UserVerifyToken, UserViewSet)

router = DefaultRouter()

router.register(r'users', UserViewSet)

router.register(r'genres', GenreViewSet)

router.register(r'titles', TitleViewSet)

router.register(r'categories', CategoryViewSet)

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/users/me/', UserProfileViewSet.as_view()),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserAuthViewSet.as_view()),
    path('v1/auth/token/', UserVerifyToken.as_view()),
]
