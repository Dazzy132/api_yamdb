from django.contrib import admin
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
