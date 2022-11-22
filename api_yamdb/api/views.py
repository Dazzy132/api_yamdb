from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review, Title
from users.models import User

from .permissions import (
    AuthorModeratorOrReadOnly,
    IsAdminOrSuperUser,
    IsUserProfile
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    SelfUserSerializer,
    TokenSerializer,
    UserSerializer,
)


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
            Review, pk=self.kwargs['review_id'], title=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_review().comments.select_related('author', 'review')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.get_review().pk
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    search_fields = ('username',)


class UserProfileViewSet(APIView):
    """Редактирование профиля."""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.role == 'admin' or request.user.is_superuser:
            serializer = UserSerializer(
                request.user,
                request.data,
                partial=True)
        else:
            serializer = SelfUserSerializer(
                request.user,
                request.data,
                partial=True
            )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)


class UserAuthViewSet(generics.CreateAPIView):
    """ViewSet для работы с созданием пользователей (или созданными через
    админ права пользователями) для их полноценной регистрации через отправки
    кода на почту"""

    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        # Проверка на то, что пользователь уже зарегистрирован
        user = User.objects.filter(username=username, email=email)
        if not user.exists():
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=HTTPStatus.BAD_REQUEST
                )
            serializer.save()
            user = get_object_or_404(User, username=username, email=email)
        else:
            user = user[0]
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш токен: {confirmation_code}',
            'auth@yamdb.com',
            [email],
            fail_silently=False,
        )
        return Response(
            {'username': username, 'email': email},
            status=HTTPStatus.OK
        )


class UserVerifyToken(generics.CreateAPIView):
    """ViewSet для выдачи JWT токенов"""

    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
        user = get_object_or_404(User, username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')

        if default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'token': str(RefreshToken.for_user(user).access_token)},
                status=HTTPStatus.OK
            )
        return Response(
            {'error': 'Введен неправильный код'},
            status=HTTPStatus.BAD_REQUEST
        )
