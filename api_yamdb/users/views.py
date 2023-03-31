from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrSuperUser
from .serializers import UserSerializer, TokenSerializer, SignUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
        else:
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    """Функция для регистрации/авторизации пользователей для последующей
    отправки кода им на почту."""
    user = User.objects.filter(**request.data)
    if not user.exists():
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(User, username=request.data.get('username'))
    else:
        user = user[0]
        serializer = SignUpSerializer(user)
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
    user = get_object_or_404(
        User, username=serializer.validated_data.get('username')
    )
    token = RefreshToken.for_user(user).access_token
    return Response({'token': str(token)}, status=HTTPStatus.OK)
