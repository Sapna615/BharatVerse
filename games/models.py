from django.db import models
from quizzes.models import Quiz
from culture.models import State, CulturalCategory

class Game(models.Model):
    GAME_TYPES = (
        ('picture_puzzle', 'Picture Puzzle'),
        ('crossword', 'Cultural Crossword'),
        ('word_search', 'Word Search'),
        ('timeline', 'Heritage Timeline Challenge'),
        ('match_culture', 'Match the Culture'),
        ('guess_dance', 'Guess the Dance'),
        ('sound_india', 'Sound of India'),
        ('taste_india', 'Taste of India'),
        ('craft_detective', 'Craft Detective'),
        ('heritage_quest', 'Heritage Quest'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    game_type = models.CharField(max_length=50, choices=GAME_TYPES)
    description = models.TextField()
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name='game_link', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(CulturalCategory, on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='games/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_game_type_display()})"
