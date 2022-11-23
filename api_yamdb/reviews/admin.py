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


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('author',)


class ReviewsInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('author',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Category"""
    list_display: Fields = ['name', 'slug']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Genres"""
    list_display: Fields = ['name', 'slug']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Title"""
    list_display: Fields = ['id', 'name', 'year', 'pub_date', 'category']
    filter_horizontal: Fields = ['genre']
    ordering: Fields = ['name', 'year', 'pub_date', 'category']
    list_per_page: int = 10
    search_fields: Fields = ['name']
    inlines = [ReviewsInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Модель комментариев в админке"""
    list_display = ('id', 'text', 'pub_date')
    readonly_fields = ('pub_date',)
    search_fields = ('text',)
    save_as = True


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Модель отзывов в админке"""
    list_display = ('id', 'text', 'pub_date')
    readonly_fields = ('pub_date',)
    search_fields = ('text',)
    save_as = True
    inlines = [CommentsInline]


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Genres"""
    list_display: Fields = ['title', 'genre']
