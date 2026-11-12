from django.db import models
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

class CulturalMedia(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    )
    cultural_entry = models.ForeignKey(CulturalEntry, on_delete=models.CASCADE, related_name='media_items')
    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    provider = models.CharField(max_length=100, blank=True)
    external_url = models.URLField(blank=True, help_text="e.g. YouTube URL")
    file = models.FileField(upload_to='cultural_media/', blank=True, null=True)
    description = models.TextField(blank=True)
    attribution = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.media_type})"


class LiteraryWork(models.Model):
    WORK_TYPE_CHOICES = (
        ('book', 'Classical Literature & Poetry'),
        ('sacred_text', 'Sacred Text & Philosophical Tradition'),
        ('manuscript', 'Historical Manuscript & Archive'),
        ('oral_tradition', 'Oral Literature & Folklore'),
        ('treatise', 'Traditional Knowledge & Science'),
    )
    CLASSIFICATION_CHOICES = (
        ('original', 'Original Composition'),
        ('translation', 'Authorized Translation'),
        ('retelling', 'Regional Retelling / Recension'),
        ('commentary', 'Philosophical Commentary'),
        ('critical_edition', 'Critical / Modern Edition'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    author_creator = models.CharField(max_length=250, blank=True, help_text="Author, poet, compiler, or tradition attribution")
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES, default='book')
    tradition = models.CharField(max_length=120, blank=True, help_text="e.g. Hindu, Sikh, Buddhist, Jain, Islamic, Christian, Tribal/Folk, Classical")
    language = models.CharField(max_length=100)
    script = models.CharField(max_length=100, blank=True)
    historical_period = models.CharField(max_length=150, blank=True, help_text="e.g. 5th Century BCE, Sangam Era, 16th Century CE")
    classification_type = models.CharField(max_length=50, choices=CLASSIFICATION_CHOICES, default='original')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='literary_works', help_text="Regional association if geographically rooted. Null for Pan-Indian / National texts.")
    category = models.ForeignKey(CulturalCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='literary_works')
    brief_intro = models.CharField(max_length=350)
    synopsis = models.TextField()
    cultural_significance = models.TextField()
    historical_context = models.TextField(blank=True)
    themes = models.TextField(blank=True)
    available_translations = models.TextField(blank=True, help_text="Known translations and regional retellings")
    custodian_collection = models.CharField(max_length=250, blank=True, help_text="Custodial archive, library, or living community")
    rights_attribution = models.CharField(max_length=250, default="Public Domain / Authorized Educational Archive")
    excerpt_content = models.TextField(blank=True, help_text="Public domain read-along text, opening cantos, or authorized verses")
    external_reading_url = models.URLField(blank=True, help_text="Lawful reading link or digital archive repository")
    image = models.ImageField(upload_to='library/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    featured = models.BooleanField(default=False)
    related_entries = models.ManyToManyField(CulturalEntry, blank=True, related_name='connected_literature')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.language})"

