from django.contrib import admin
from .models import State, CulturalCategory, CulturalEntry, Festival, Tradition, FolkArt, Cuisine, CulturalConnection, CulturalStory, CulturalCalendarEvent, CulturalMedia, LiteraryWork

@admin.register(LiteraryWork)
class LiteraryWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_creator', 'language', 'work_type', 'tradition', 'status', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author_creator', 'language', 'synopsis', 'cultural_significance')
    list_filter = ('work_type', 'tradition', 'classification_type', 'status', 'featured', 'state')
    filter_horizontal = ('related_entries',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'is_featured', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'region')
    list_filter = ('region', 'is_featured')

@admin.register(CulturalCategory)
class CulturalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class CulturalMediaInline(admin.TabularInline):
    model = CulturalMedia
    extra = 1
    fields = ('title', 'media_type', 'provider', 'external_url', 'file', 'display_order', 'is_active', 'is_featured')

@admin.register(CulturalEntry)
class CulturalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'state', 'status', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')
    list_filter = ('status', 'featured', 'category', 'state')
    inlines = [CulturalMediaInline]

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'month', 'featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'month')
    list_filter = ('featured', 'state')

@admin.register(Tradition)
class TraditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(FolkArt)
class FolkArtAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(CulturalConnection)
class CulturalConnectionAdmin(admin.ModelAdmin):
    list_display = ('source_entry', 'relationship_type', 'target_entry')
    search_fields = ('source_entry__title', 'target_entry__title', 'relationship_type')
    list_filter = ('relationship_type',)

@admin.register(CulturalStory)
class CulturalStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'state', 'category', 'moderation_status', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('moderation_status', 'featured', 'state', 'category')

@admin.register(CulturalCalendarEvent)
class CulturalCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'month', 'date', 'state', 'category')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'month')
    list_filter = ('month', 'state', 'category')
