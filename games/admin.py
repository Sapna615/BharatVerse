from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'game_type', 'is_active', 'created_at')
    list_filter = ('game_type', 'is_active', 'state')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
