from django.db import models
from django.conf import settings
from culture.models import CulturalEntry

class CulturalJourney(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journeys')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    progress = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class JourneyItem(models.Model):
    journey = models.ForeignKey(CulturalJourney, on_delete=models.CASCADE, related_name='items')
    cultural_entry = models.ForeignKey(CulturalEntry, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('journey', 'cultural_entry')
        ordering = ['order']
        
    def __str__(self):
        return f"{self.journey.title} - {self.cultural_entry.title}"
