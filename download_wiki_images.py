import os
import django
import urllib.request
from urllib.parse import urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game

images = {
    'bamboo-craft': 'https://upload.wikimedia.org/wikipedia/commons/e/e0/Bamboo_craft_of_Assam.jpg',
    'banarasi-saree': 'https://upload.wikimedia.org/wikipedia/commons/5/5f/Banarasi_Sari.jpg',
    'ancient-manuscript': 'https://upload.wikimedia.org/wikipedia/commons/2/25/Rigveda_MS2097.jpg',
    'folk-story': 'https://upload.wikimedia.org/wikipedia/commons/b/b8/Pattachitra_Painting.jpg',
    'identify-the-instrument': 'https://upload.wikimedia.org/wikipedia/commons/b/b2/Sitar_%28Music_Instrument%29.jpg',
    'guess-the-dance-form': 'https://upload.wikimedia.org/wikipedia/commons/f/fc/Kathakali_performance.jpg',
    'match-the-region': 'https://upload.wikimedia.org/wikipedia/commons/5/55/India_map_en.svg'
}

req_headers = {'User-Agent': 'Mozilla/5.0'}

for slug, url in images.items():
    try:
        ext = url.split('.')[-1]
        filename = f"{slug}.{ext}"
        filepath = os.path.join('/app/media/games', filename)
        
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        
        # Find game by slug or something containing slug
        game = Game.objects.filter(slug__icontains=slug).first()
        if game:
            game.thumbnail = f"games/{filename}"
            game.save()
            print(f"Updated {game.title} with {filename}")
        else:
            print(f"Game not found for slug {slug}")
    except Exception as e:
        print(f"Error for {slug}: {e}")

