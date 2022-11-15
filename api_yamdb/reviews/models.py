from django.db import models


class Categories(models.Model):
    """Категории для произведений"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        'Категория произведения',
        max_length=200,
        help_text='Выберите категорию произведения'
    )
    slug = models.SlugField(
        'Адрес категории произведения',
        unique=True
    )
    description = models.TextField(
        'Описание категории',
        max_length=400
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    """Жанры для произведений"""
    ROCK = 'RO'
    FANTSY = 'FA'
    ARTHOUSE = 'AR'
    OUTOFGENRE = 'OU'
    GENRES_CHOICES = [
        (ROCK, 'Rock'),
        (FANTSY, 'Fantasy'),
        (ARTHOUSE, 'Arthouse')
        (OUTOFGENRE, 'Out of genre')
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        'Жанр произведения',
        max_length=200,
        help_text='Выберите жанр произведения'
    )
    genres = models.CharField(
        max_length=2,
        choices=GENRES_CHOICES,
        default=OUTOFGENRE,
    )
    description = models.TextField(
        'Описание жанра',
        max_length=400
    )

    def __str__(self) -> str:
        return self.genres

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    """Модель для произведений"""
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    year = models.IntegerField('Год создания произведения', null=True, blank=True, default=2022)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        1, on_delete=models.CASCADE, related_name='titles')
    genres = models.ManyToManyField(
        Genres,
        verbose_name='Жанр произведения',
        blank=False,
        null=True,
        related_name='genres',
        help_text='Выберите жанр произведения'
    )
    categories = models.ForeignKey(
        Categories,
        verbose_name='Категория произведения',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        help_text='Выберите категорию произведения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
