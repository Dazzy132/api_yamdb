from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet, UserViewSet, UserAuthViewSet, UserVerifyToken, UserProfileViewSet, GenreViewSet, TitleViewSet, CategoryViewSet

router = DefaultRouter()

router.register(
    r'users/me',
    UserProfileViewSet,
    basename='user-profile'
)

router.register(
    r'users',
    UserViewSet
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)

router.register(
    r'genres',
    GenreViewSet
)

router.register(
    r'titles',
    TitleViewSet
)

router.register(
    r'categories',
    CategoryViewSet
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserAuthViewSet.as_view()),
    path('v1/auth/token/', UserVerifyToken.as_view()),
]