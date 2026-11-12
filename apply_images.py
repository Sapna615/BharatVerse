import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game

def update_game(slug_part, image_name):
    game = Game.objects.filter(slug__icontains=slug_part).first()
    if game:
        game.thumbnail = f"games/{image_name}"
        game.save()
        print(f"Updated {game.title} with {image_name}")

update_game('diwali', 'diwali_up.jpg')
update_game('sitar', 'sitar_maharashtra.jpg')
update_game('warli', 'warli_art.jpg')
