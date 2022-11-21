from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review, Title
from users.models import User

from .permissions import AuthorOrReadOnly, IsAdminOrSuperUser, IsUserProfile
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TokenSerializer,
    UserSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.select_related('author', 'title')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title_id=self.get_title().pk)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

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
    # Поле по которому можно осуществлять детальный поиск
    lookup_field = 'username'

    # # при detail True не работает отображение
    # @action(detail=False,
    #         methods=['GET', 'PUT', 'PATCH'],
    #         url_path=r'me',
    #         permission_classes=[IsUserProfile]
    #         )
    # def user_profile(self, request, pk=None):
    #     user = get_object_or_404(User, username=request.user)
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         return Response(serializer.data, status=200)
    #     return Response(serializer.errors, status=400)
    #
    # def get_permissions(self):
    #     permission_classes = [IsUserProfile]
    #
    #     # if self.action not in SAFE_METHODS:
    #     #     permission_classes = [IsAdminOrSuperUser]
    #     return [permission() for permission in permission_classes]


class UserProfileViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    """Редактирование профиля."""

    serializer_class = UserSerializer
    permission_classes = (IsUserProfile,)

    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        return user


class UserAuthViewSet(generics.CreateAPIView):
    """ViewSet для работы с созданием пользователей (или созданными через
    админ права пользователями) для их полноценной регистрации через отправки
    кода на почту"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

        email = request.data.get('email')
        username = request.data.get('username')

        # Проверка на то, если пользователь уже зарегистрирован
        user = User.objects.filter(username=username, email=email)
        if not user.exists():
            serializer.save()
            user = get_object_or_404(User, username=username, email=email)
        else:
            user = user[0]
        confirmation_code = default_token_generator.make_token(
            get_object_or_404(User, username=username, email=email)
        )
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
