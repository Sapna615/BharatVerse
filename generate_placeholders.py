import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game
from quizzes.models import Quiz

def create_placeholder(title, filename):
    img = Image.new('RGB', (800, 600), color=(26, 41, 66)) # Bharat Navy
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Simple text wrap
    words = title.split()
    lines = []
    line = ''
    for word in words:
        if d.textlength(line + word, font=font) < 700:
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    
    y = 250 - (len(lines)*25)
    for line in lines:
        w = d.textlength(line, font=font)
        d.text(((800-w)/2, y), line, fill=(255,153,51), font=font) # Saffron text
        y += 60
        
    filepath = os.path.join('/app/media/games', filename)
    img.save(filepath)
    return f"games/{filename}"

# Broken games
broken_games = ['bamboo-craft', 'banarasi-saree-pattern', 'ancient-manuscript', 'folk-story-illustration']
for slug in broken_games:
    game = Game.objects.filter(slug__icontains=slug).first()
    if game:
        path = create_placeholder(game.title, f"{slug}.jpg")
        game.thumbnail = path
        game.save()
        print(f"Placeholder created for Game: {game.title}")

# Broken quizzes
broken_quizzes = ['match-region-demo', 'guess-dance-demo', 'sound-india-demo']
for slug in broken_quizzes:
    quiz = Quiz.objects.filter(slug=slug).first()
    if quiz:
        path = create_placeholder(quiz.title, f"quiz_{slug}.jpg")
        quiz.image = path
        quiz.save()
        print(f"Placeholder created for Quiz: {quiz.title}")
