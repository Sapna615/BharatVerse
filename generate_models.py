import os

BASE_DIR = '/Users/sapnarai/BharatVerse'

accounts_models = """from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('explorer', 'Explorer'),
        ('contributor', 'Contributor'),
        ('curator', 'Curator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='explorer')
    bio = models.TextField(blank=True)
    region = models.CharField(max_length=100, blank=True)
    interests = models.JSONField(default=list, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    xp = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
"""

culture_models = """from django.db import models
from django.conf import settings

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=100)
    description = models.TextField()
    cultural_summary = models.TextField()
    image = models.ImageField(upload_to='states/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class CulturalCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CulturalEntry(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(CulturalCategory, on_delete=models.CASCADE, related_name='entries')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='entries')
    short_description = models.TextField()
    detailed_story = models.TextField()
    cultural_significance = models.TextField()
    practice_description = models.TextField()
    image = models.ImageField(upload_to='culture/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Festival(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='festivals')
    month = models.CharField(max_length=50)
    description = models.TextField()
    cultural_significance = models.TextField()
    image = models.ImageField(upload_to='festivals/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Tradition(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='traditions')
    description = models.TextField()
    story = models.TextField()
    image = models.ImageField(upload_to='traditions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class FolkArt(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='folk_arts')
    description = models.TextField()
    technique = models.TextField()
    cultural_context = models.TextField()
    image = models.ImageField(upload_to='folk_arts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cuisines')
    description = models.TextField()
    ingredients = models.TextField()
    cultural_context = models.TextField()
    image = models.ImageField(upload_to='cuisines/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CulturalConnection(models.Model):
    source_entry = models.ForeignKey(CulturalEntry, related_name='source_connections', on_delete=models.CASCADE)
    target_entry = models.ForeignKey(CulturalEntry, related_name='target_connections', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source_entry', 'target_entry', 'relationship_type')
        
    def __str__(self):
        return f"{self.source_entry} -> {self.relationship_type} -> {self.target_entry}"

class CulturalStory(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    category = models.ForeignKey(CulturalCategory, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    moderation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CulturalCalendarEvent(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    month = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(CulturalCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='calendar/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
"""

exploration_models = """from django.db import models
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
"""

quizzes_models = """from django.db import models
from django.conf import settings
from culture.models import CulturalCategory

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(CulturalCategory, on_delete=models.SET_NULL, null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    image = models.ImageField(upload_to='quizzes/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    TYPE_CHOICES = (
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('image', 'Image Identification')
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='mcq')
    explanation = models.TextField(blank=True)
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.question_text

class QuizOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.option_text

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.quiz.title} - {self.score}"
"""

journeys_models = """from django.db import models
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
"""

gamification_models = """from django.db import models
from django.conf import settings

class Quest(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    requirement = models.CharField(max_length=255)
    xp = models.IntegerField(default=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Achievement(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    xp_reward = models.IntegerField(default=100)
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
        
    def __str__(self):
        return f"{self.user} - {self.achievement.name}"
"""

contributions_models = """from django.db import models
from django.conf import settings

class Submission(models.Model):
    TYPE_CHOICES = (
        ('tradition', 'Tradition'),
        ('festival', 'Festival'),
        ('story', 'Story'),
        ('cuisine', 'Cuisine'),
        ('craft', 'Craft'),
        ('folk_art', 'Folk Art'),
        ('other', 'Other'),
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
"""

files = {
    'accounts/models.py': accounts_models,
    'culture/models.py': culture_models,
    'exploration/models.py': exploration_models,
    'quizzes/models.py': quizzes_models,
    'journeys/models.py': journeys_models,
    'gamification/models.py': gamification_models,
    'contributions/models.py': contributions_models,
}

for filepath, content in files.items():
    full_path = os.path.join(BASE_DIR, filepath)
    with open(full_path, 'w') as f:
        f.write(content)
    print(f"Wrote {full_path}")
