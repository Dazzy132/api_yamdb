from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'date_joined', 'is_staff')
    list_editable = ('role',)

    def save_model(self, request, obj, form, change):
        if obj.role in ('admin', 'moderator'):
            obj.is_staff = True
            obj.save()
        else:
            obj.is_staff = False
            obj.save()
