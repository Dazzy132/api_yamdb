from django.db import models


class BaseModelReview(models.Model):
    text = models.TextField('Текст', blank=False)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True


class BaseModelUnique(models.Model):
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField('slug', unique=True)

    class Meta:
        abstract = True
