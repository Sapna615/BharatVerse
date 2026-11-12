from django.db import models
from django.conf import settings
from culture.models import CulturalEntry

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    cultural_entry = models.ForeignKey(CulturalEntry, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cultural_entry')

    def __str__(self):
        return f"{self.user} - {self.cultural_entry}"
