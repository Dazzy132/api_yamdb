from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Категории для произведений"""

    name = models.CharField(
        'Категория произведения',
        max_length=400,
        help_text='Выберите категорию произведения',
    )
    slug = models.SlugField('Адрес категории произведения', unique=True)

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name: str = 'Категория'
        verbose_name_plural: str = 'Категории'
        ordering = ('pk',)


class Genre(models.Model):
    """Модель для жанров"""

    slug = models.SlugField('Адрес жанра произведения', unique=True)
    name = models.CharField(
        'Жанр произведения',
        max_length=200,
        help_text='Выберите жанр произведения'
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name: str = 'Жанр'
        verbose_name_plural: str = 'Жанры'
        ordering = ('pk',)


class Title(models.Model):
    """Модель для произведений"""

    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        'Год создания произведения',
        blank=False,
        default=2022,
        validators=[MaxValueValidator(2022)],
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now=True)
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        verbose_name='Жанр произведения',
        related_name='titles',
        blank=False
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        help_text='Выберите категорию произведения',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = 'Произведение'
        verbose_name_plural: str = 'Произведения'
        ordering = ('pk',)


class GenreTitle(models.Model):
    """Жанры для произведений"""

    title = models.ForeignKey(
        Title,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ForeignKey(
        Genre,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name: str = 'Жанр и Произведение'
        verbose_name_plural: str = 'Жанры и произведения'


class Review(models.Model):
    """Модель отзывов"""

    text = models.TextField(
        'Текст отзыва',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pk',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(models.Model):
    """Модель комментариев"""

    text = models.TextField(
        'Комментарий',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        related_name='comments',
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pk',)
