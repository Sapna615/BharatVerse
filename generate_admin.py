import os

BASE_DIR = '/Users/sapnarai/BharatVerse'

accounts_admin = """from django.contrib import admin
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
"""

culture_admin = """from django.contrib import admin
from .models import State, CulturalCategory, CulturalEntry, Festival, Tradition, FolkArt, Cuisine, CulturalConnection, CulturalStory, CulturalCalendarEvent

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

@admin.register(CulturalEntry)
class CulturalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'state', 'status', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')
    list_filter = ('status', 'featured', 'category', 'state')

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
"""

exploration_admin = """from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cultural_entry', 'created_at')
    search_fields = ('user__username', 'cultural_entry__title')
    list_filter = ('created_at',)
"""

quizzes_admin = """from django.contrib import admin
from .models import Quiz, Question, QuizOption, QuizAttempt

class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 3

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    list_filter = ('difficulty', 'is_active', 'category')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'order')
    list_filter = ('quiz', 'question_type')
    search_fields = ('question_text',)
    inlines = [QuizOptionInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'percentage', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('user__username',)
"""

journeys_admin = """from django.contrib import admin
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
"""

gamification_admin = """from django.contrib import admin
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
"""

contributions_admin = """from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'contributor', 'submission_type', 'state', 'moderation_status', 'created_at')
    search_fields = ('title', 'content', 'contributor__username')
    list_filter = ('moderation_status', 'submission_type', 'state')
    readonly_fields = ('created_at', 'reviewed_at')
    
    def save_model(self, request, obj, form, change):
        if change and 'moderation_status' in form.changed_data:
            from django.utils import timezone
            obj.reviewer = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
"""

files = {
    'accounts/admin.py': accounts_admin,
    'culture/admin.py': culture_admin,
    'exploration/admin.py': exploration_admin,
    'quizzes/admin.py': quizzes_admin,
    'journeys/admin.py': journeys_admin,
    'gamification/admin.py': gamification_admin,
    'contributions/admin.py': contributions_admin,
}

for filepath, content in files.items():
    full_path = os.path.join(BASE_DIR, filepath)
    with open(full_path, 'w') as f:
        f.write(content)
    print(f"Wrote {full_path}")
