from django.db import models
from django.conf import settings

class Submission(models.Model):
    TYPE_CHOICES = (
        ('tradition', 'Tradition'),
        ('festival', 'Festival'),
        ('story', 'Story & Folklore'),
        ('cuisine', 'Cuisine'),
        ('craft', 'Craft & Textile'),
        ('folk_art', 'Folk Art & Painting'),
        ('literature', 'Book & Literary Work'),
        ('manuscript', 'Manuscript & Historical Document'),
        ('oral_history', 'Oral History & Community Memory'),
        ('traditional_practice', 'Traditional Knowledge System'),
        ('other', 'Other Heritage'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    submission_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='submissions/', blank=True, null=True)
    source_note = models.TextField(blank=True)
    consent_given = models.BooleanField(default=False)
    moderation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_submissions')
    review_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
