import os
import django
import urllib.request
import urllib.parse
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game
from quizzes.models import Quiz

def fetch_wiki_image(query, filename):
    try:
        # Step 1: Search for the article
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'BharatVerse/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            if not data['query']['search']:
                return False
            title = data['query']['search'][0]['title']
            
        # Step 2: Get image from the article
        image_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=800"
        req = urllib.request.Request(image_url, headers={'User-Agent': 'BharatVerse/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            if 'thumbnail' in pages[page_id]:
                img_src = pages[page_id]['thumbnail']['source']
                
                # Step 3: Download image
                filepath = os.path.join('/app/media/games', filename)
                req_img = urllib.request.Request(img_src, headers={'User-Agent': 'BharatVerse/1.0'})
                with urllib.request.urlopen(req_img) as img_res, open(filepath, 'wb') as out:
                    out.write(img_res.read())
                return True
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return False

# Update games
games_to_update = {
    'bamboo-craft': 'Bamboo weaving Assam',
    'banarasi-saree': 'Banarasi sari',
    'ancient-manuscript': 'Rigveda manuscript',
    'folk-story': 'Pattachitra',
    'find-the-dances': 'Indian classical dance',
    'find-the-festivals': 'Diwali',
    'explore-punjab': 'Bhangra (dance)',
    'match-the-region': 'Political Map of India',
    'guess-the-dance': 'Kathakali',
    'identify-the-instrument': 'Sitar'
}

for slug, query in games_to_update.items():
    game = Game.objects.filter(slug__icontains=slug).first()
    if game:
        filename = f"{slug}_wiki.jpg"
        if fetch_wiki_image(query, filename):
            game.thumbnail = f"games/{filename}"
            game.save()
            print(f"Successfully updated Game: {game.title}")
        else:
            print(f"Failed to find image for Game: {game.title}")

# Update Quizzes
quizzes_to_update = {
    'match-region-demo': 'Political Map of India',
    'guess-dance-demo': 'Kathakali',
    'sound-india-demo': 'Sitar',
    'india-cultural-quiz': 'Culture of India'
}

for slug, query in quizzes_to_update.items():
    quiz = Quiz.objects.filter(slug=slug).first()
    if quiz:
        filename = f"quiz_{slug}_wiki.jpg"
        if fetch_wiki_image(query, filename):
            quiz.image = f"games/{filename}"
            quiz.save()
            print(f"Successfully updated Quiz: {quiz.title}")
        else:
            print(f"Failed to find image for Quiz: {quiz.title}")

