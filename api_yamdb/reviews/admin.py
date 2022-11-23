from typing import NamedTuple

from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class Fields(NamedTuple):
    """Типизация для полей admin"""
    name: str
    year: str
    pub_date: str
    author: str
    category: str
    genre: str
    slug: str
    text: str


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
    list_display: Fields = ('id', 'text', 'pub_date')
    readonly_fields: Fields = ('pub_date',)
    search_fields: Fields = ('text',)
    save_as = True


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Модель отзывов в админке"""
    list_display: Fields = ('id', 'text', 'pub_date')
    readonly_fields: Fields = ('pub_date',)
    search_fields: Fields = ('text',)
    save_as = True
    inlines = [CommentsInline]


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Регистрация в admin модели Genres"""
    list_display: Fields = ['title', 'genre']
