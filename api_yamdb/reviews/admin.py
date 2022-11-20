from django.contrib import admin
from typing import NamedTuple

from .models import Categories, Genres, Title, GenreTitle


class Fields(NamedTuple):
    """Типизация для полей admin"""
    name: str
    year: str
    pub_date: str
    author: str
    category: str
    genre: str
    slug: str


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Categories"""
    list_display: Fields = ['name', 'slug']


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Genres"""
    list_display: Fields = ['name', 'slug']


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Titles"""
    list_display: Fields = ['name', 'year', 'pub_date', 'category']
    filter_horizontal: Fields = ['genre']
    ordering: Fields = ['name', 'year', 'pub_date', 'category']
    list_per_page: int = 10
    search_fields: Fields = ['name']

from .models import Comment, Review


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Модель комментариев в админке"""
    list_display = ('text', 'pub_date')
    readonly_fields = ('pub_date',)
    search_fields = ('text',)
    save_as = True


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Модель отзывов в админке"""
    list_display = ('text', 'pub_date')
    readonly_fields = ('pub_date',)
    search_fields = ('text',)
    save_as = True


# @admin.register(Rating)
# class ReviewAdmin(admin.ModelAdmin):
#     """Модель отзывов в админке"""
#     list_display = ('score',)

