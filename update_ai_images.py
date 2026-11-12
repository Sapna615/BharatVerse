import os
import django
import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game

def get_filename(pattern):
    files = glob.glob(f'/app/media/games/{pattern}')
    if files:
        return f"games/{os.path.basename(files[0])}"
    return None

updates = {
    'kathakali-dance-puzzle-puzzle': get_filename('kathakali*.jpg'),
    'gujarati-thali-puzzle-puzzle': get_filename('gujarati*.jpg'),
}

for slug, img_path in updates.items():
    if img_path:
        game = Game.objects.filter(slug=slug).first()
        if game:
            game.thumbnail = img_path
            game.save()
            print(f"Updated {slug} with AI image {img_path}")

