import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game
from culture.models import State, CulturalCategory

print("Seeding Word Searches...")

categories_to_seed = ['Dance', 'Festival']
for cat_name in categories_to_seed:
    cat = CulturalCategory.objects.filter(name__icontains=cat_name).first()
    state = State.objects.first()
    if cat:
        slug = f"word-search-{cat.slug}"
        if not Game.objects.filter(slug=slug).exists():
            Game.objects.create(
                title=f"Find the {cat.name}s",
                slug=slug,
                game_type='word_search',
                description=f"Search for hidden {cat.name.lower()} vocabulary.",
                state=state,
                category=cat,
            )
            print(f"Created word search for {cat.name}")

# Seed one for states
state = State.objects.first()
slug = f"word-search-{state.slug}"
if not Game.objects.filter(slug=slug).exists():
    Game.objects.create(
        title=f"Explore {state.name}",
        slug=slug,
        game_type='word_search',
        description=f"Find words related to {state.name}.",
        state=state,
        category=CulturalCategory.objects.first()
    )
    print(f"Created word search for {state.name}")
    
print("Done seeding word searches!")
