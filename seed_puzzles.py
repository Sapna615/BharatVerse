import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game
from culture.models import State, CulturalCategory

print("Seeding puzzles for all categories...")
state = State.objects.first()
categories = CulturalCategory.objects.all()

for cat in categories:
    slug = f"{cat.slug}-puzzle-demo"
    if not Game.objects.filter(slug=slug).exists():
        Game.objects.create(
            title=f"{cat.name} Puzzle",
            slug=slug,
            game_type='picture_puzzle',
            description=f"Reconstruct this beautiful image representing {cat.name}.",
            state=state,
            category=cat,
            thumbnail='games/taj_mahal_1791472732183.jpg'
        )
        print(f"Created puzzle for {cat.name}")

print("Done seeding puzzles!")
