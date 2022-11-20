from django.db import models
from django.core.validators import MaxValueValidator


class Categories(models.Model):
    """Категории для произведений"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        'Категория произведения',
        max_length=200,
        help_text='Выберите категорию произведения'
    )
    slug = models.SlugField(
        'Адрес категории произведения',
        unique=True
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name: str = 'Категория'
        verbose_name_plural: str = 'Категории'


class Genres(models.Model):
    """Модель для жанров"""
    ROCK: str = 'RO'
    FANTSY: str = 'FA'
    ARTHOUSE: str = 'AR'
    OUTOFGENRE: str = 'OU'
    GENRES_CHOICES: tuple = [
        (ROCK, 'Rock'),
        (FANTSY, 'Fantasy'),
        (ARTHOUSE, 'Arthouse'),
        (OUTOFGENRE, 'Out Of Genre'),
    ]
    id = models.AutoField(primary_key=True)
    # Скорее всего, надо убрать choices
    slug = models.SlugField(
        max_length=2,
        choices=GENRES_CHOICES,
        default=OUTOFGENRE,
    )
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


class Title(models.Model):
    """Модель для произведений"""
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    year = models.IntegerField(
        'Год создания произведения',
        blank=False,
        default=2022,
        validators=[MaxValueValidator(2022)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now=True)
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр произведения',
        blank=True,
        related_name='genre',
        help_text='Выберите жанр произведения'
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория произведения',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
        help_text='Выберите категорию произведения'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = 'Произведение'
        verbose_name_plural: str = 'Произведения'


class GenreTitle(models.Model):
    """Жанры для произведений"""
    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(
        Title,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ForeignKey(
        Genres,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name: str = 'Жанр и Прозведение'
        verbose_name_plural: str = 'Жанры и произведения'
