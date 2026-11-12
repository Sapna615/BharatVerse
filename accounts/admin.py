from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'xp', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'region')
    fieldsets = UserAdmin.fieldsets + (
        ('BharatVerse Profile', {'fields': ('role', 'bio', 'region', 'interests', 'avatar', 'xp')}),
    )
