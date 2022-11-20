from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    """Модель отзывов"""
    text = models.TextField('Текст отзыва',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    # author = models.ForeignKey(
    #     User,
    #     related_name='reviews',
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор',
    # )

    author = models.CharField('Имя автора', max_length=50, blank=False)

    # title = models.ForeignKey(
    #     Title,
    #     related_name='reviews',
    #     verbose_name='Произведение',
    #     on_delete=models.CASCADE,
    # )

    title = models.IntegerField('ID произведения', blank=False)

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


class Comment(models.Model):
    """Модель комментариев"""
    text = models.TextField('Комментарий',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    # author = models.ForeignKey(
    #     User,
    #     related_name='comments'
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор',
    # )

    author = models.CharField('Имя автора', max_length=50, blank=False)

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
