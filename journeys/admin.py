from django.contrib import admin
from .models import CulturalJourney, JourneyItem

class JourneyItemInline(admin.TabularInline):
    model = JourneyItem
    extra = 1

@admin.register(CulturalJourney)
class CulturalJourneyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'progress', 'is_public', 'created_at')
    search_fields = ('title', 'user__username')
    list_filter = ('is_public',)
    inlines = [JourneyItemInline]
