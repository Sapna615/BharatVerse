import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game

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

title = "Ancient India Crossword"
slug = "ancient-india-crossword"
thumbnail = create_placeholder(title, f"{slug}_card.jpg")

game, created = Game.objects.get_or_create(
    slug=slug,
    defaults={
        'title': title,
        'game_type': 'crossword',
        'description': 'Solve clues to reveal ancient Indian heritage!',
        'thumbnail': thumbnail,
        'is_active': True
    }
)
print("Crossword created!" if created else "Crossword already exists.")
