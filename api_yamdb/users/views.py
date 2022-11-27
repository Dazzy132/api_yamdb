from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrSuperUser
from .serializers import SelfUserSerializer, UserSerializer, TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    search_fields = ('username',)


class UserProfileViewSet(APIView):
    """Редактирование профиля."""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_admin or request.user.is_superuser:
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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    """Функция для регистрации/авторизации пользователей для последующей
    отправки кода им на почту."""
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # Получить или создать пользователя '_' - когда имя переменной неважно
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Код подтверждения: {confirmation_code}',
        'auth@yamdb.com',
        [user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Функция для получения JWT токена. APIView тянет за собой не нужное, по
    этому проще реализовать это через декораторы и функцию"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = RefreshToken.for_user(request.user).access_token
    return Response({'token': str(token)}, status=HTTPStatus.OK)
