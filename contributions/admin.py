from django.contrib import admin
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
