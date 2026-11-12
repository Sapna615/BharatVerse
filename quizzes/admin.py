from django.contrib import admin
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
