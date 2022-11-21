from django.contrib import admin
from typing import NamedTuple

from .models import Category, Genre, Title, GenreTitle, Comment, Review


class Fields(NamedTuple):
    """Типизация для полей admin"""
    name: str
    year: str
    pub_date: str
    author: str
    category: str
    genre: str
    slug: str


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Category"""
    list_display: Fields = ['name', 'slug']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Genres"""
    list_display: Fields = ['name', 'slug']


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Title"""
    list_display: Fields = ['name', 'year', 'pub_date', 'category']
    filter_horizontal: Fields = ['genre']
    ordering: Fields = ['name', 'year', 'pub_date', 'category']
    list_per_page: int = 10
    search_fields: Fields = ['name']


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


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Genres"""
    list_display: Fields = ['title', 'genre']
