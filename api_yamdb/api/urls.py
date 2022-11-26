from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reviews.views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import (sign_up, UserProfileViewSet, get_token,
                         UserViewSet)

from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)

router.register(r'genres', GenreViewSet)

router.register(r'titles', TitleViewSet, basename='titles')

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
    path('v1/users/me/', UserProfileViewSet.as_view(),),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up),
    path('v1/auth/token/', get_token),
]
