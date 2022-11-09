from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_moder', 'last_login']
    list_display_links = ['id', 'username']
    list_filter = ['is_staff', 'is_moder']
    search_fields = ['username']
    save_as = True
