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

# Update empty Games
for game in Game.objects.filter(thumbnail=''):
    path = create_placeholder(game.title, f"{game.slug}_card.jpg")
    game.thumbnail = path
    game.save()
    print(f"Placeholder created for Game: {game.title}")

# Update empty Quizzes
for quiz in Quiz.objects.filter(image=''):
    path = create_placeholder(quiz.title, f"quiz_{quiz.slug}_card.jpg")
    quiz.image = path
    quiz.save()
    print(f"Placeholder created for Quiz: {quiz.title}")

