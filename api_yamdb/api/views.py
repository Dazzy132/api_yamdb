from rest_framework import viewsets, generics, views
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import filters
from .permissions import IsAdminOrSuperUser, IsUserProfile, AuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Review, Comment, Genre, Title, Category
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer, GenreSerializer, TitleSerializer, CategorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from .utils import ListEditViewSet
from rest_framework.generics import RetrieveUpdateAPIView


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.select_related('author')
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny, AuthorOrReadOnly]

    def perform_create(self, serializer):
        author = serializer.validated_data.get('author')
        serializer.save(
            author=author, title=self.kwargs['title_id']
        )


class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.select_related('author')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, AuthorOrReadOnly]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        # return self.get_review().comments.select_related('author')
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.get_review().pk)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser]
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


class UserProfileViewSet(ListEditViewSet):
    """Попытка сделать на generics"""
    serializer_class = UserSerializer
    permission_classes = [IsUserProfile]

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
        email = request.data.get('email')
        username = request.data.get('username')

        # Проверка на то, если пользователь уже зарегистрирован
        user = User.objects.filter(username=username, email=email)
        if user.exists():
            return self.send_mail_user(user[0], email=email)

        # Если пользователя нет, то идет регистрация его
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=username, email=email)
            return self.send_mail_user(user, email)
        return Response(serializer.errors, status=400)

    def send_mail_user(self, user: User, email):
        """Отправить сообщение пользователю на указанный email"""
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код подтверждения для получения токена',
            message=f'Ваш токен: {confirmation_code}',
            from_email='yamdb@mail.ru',
            recipient_list=[email],
            fail_silently=False
        )
        return Response('Сообщение с кодом отправлено на почту!', status=200)


class UserVerifyToken(views.APIView):
    """ViewSet для выдачи JWT токенов"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': f'Пользователя с почтой {email} не существует'},
                status=400)

        if default_token_generator.check_token(user, confirmation_code):
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)

            return Response({'token': access_token}, status=200)
        return Response({'error': 'Введен неправильный код'}, status=400)



    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    """Viewset для модели Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    # необходимо переопределить пермишены
    permission_classes = [IsAdminOrSuperUser]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для модели Title"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    # необходимо переопределить пермишены
    permission_classes = [IsAdminOrSuperUser]
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete', 'patch']


class CategoryViewSet(viewsets.ModelViewSet):
    """Viewset для модели Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    # необходимо переопределить пермишены
    permission_classes = [IsAdminOrSuperUser]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete']
