from django.contrib import admin
from .models import Quest, Achievement, UserAchievement

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    list_filter = ('is_active',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_reward')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')
    search_fields = ('user__username', 'achievement__name')
    list_filter = ('earned_at',)
