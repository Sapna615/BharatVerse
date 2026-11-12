import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game
from culture.models import CulturalCategory

lit_cat = CulturalCategory.objects.filter(slug='literature').first()

# 1. Literary Word Search Game
ws_game, ws_created = Game.objects.get_or_create(
    slug='indian-literature-word-search',
    defaults={
        'title': 'Indian Literature & Epics Word Search',
        'game_type': 'word_search',
        'description': 'Discover foundational epics, classic manuscripts, and literary traditions of Bharat hidden in the letter matrix.',
        'category': lit_cat,
        'is_active': True
    }
)
print("Literary Word Search created!" if ws_created else "Literary Word Search exists.")

# 2. Literary Crossword Game
cw_game, cw_created = Game.objects.get_or_create(
    slug='classical-authors-crossword',
    defaults={
        'title': 'Authors & Manuscripts Crossword',
        'game_type': 'crossword',
        'description': 'Solve clues to test your mastery of India’s celebrated poets, sages, Sangam literature, and medical codices.',
        'category': lit_cat,
        'is_active': True
    }
)
print("Literary Crossword created!" if cw_created else "Literary Crossword exists.")
