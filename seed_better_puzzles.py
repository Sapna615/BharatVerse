import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from games.models import Game
from culture.models import State, CulturalCategory

# First, clean up the old demo puzzles
Game.objects.filter(slug__contains='-puzzle-demo').delete()

# Copy some artifacts to media/games
artifact_dir = '/Users/sapnarai/.gemini/antigravity-ide/brain/52831b9f-8158-4504-a9ce-2da4813aa59e/'
media_dir = '/app/media/games/'
os.makedirs(media_dir, exist_ok=True)

# Define some manual mappings to make them look real
puzzles_to_create = [
    {
        'title': 'Kathakali Dance Puzzle',
        'category_name': 'Dance',
        'state_name': 'Kerala',
        'desc': 'Piece together this beautiful Kathakali performer.',
        'image': 'media_1791475290601.png'
    },
    {
        'title': 'Sitar Instrument Puzzle',
        'category_name': 'Music',
        'state_name': 'Maharashtra',
        'desc': 'Reconstruct the classical sitar instrument.',
        'image': 'media_1791475451197.png'
    },
    {
        'title': 'Diwali Celebration',
        'category_name': 'Festival',
        'state_name': 'Uttar Pradesh',
        'desc': 'Solve the puzzle of the festival of lights.',
        'image': 'media_1791476894839.png'
    },
    {
        'title': 'Warli Art Puzzle',
        'category_name': 'Art',
        'state_name': 'Maharashtra',
        'desc': 'A classic piece of Warli tribal art.',
        'image': 'media_1791472124520.png'
    },
    {
        'title': 'Bamboo Craft',
        'category_name': 'Craft',
        'state_name': 'Assam',
        'desc': 'Traditional bamboo weaving craft puzzle.',
        'image': 'media_1791472993977.png'
    },
    {
        'title': 'Gujarati Thali Puzzle',
        'category_name': 'Cuisine',
        'state_name': 'Gujarat',
        'desc': 'A delicious spread of Gujarati cuisine.',
        'image': 'uploaded_media_1791557153937.png'  # Assuming I rename one of the imgs
    },
    {
        'title': 'Banarasi Saree Pattern',
        'category_name': 'Clothing',
        'state_name': 'Uttar Pradesh',
        'desc': 'Intricate weaving of a Banarasi Saree.',
        'image': 'uploaded_media_1791557456803.png'
    },
    {
        'title': 'Hawa Mahal Puzzle',
        'category_name': 'Architecture',
        'state_name': 'Rajasthan',
        'desc': 'The Palace of Winds in Jaipur.',
        'image': 'hawa_mahal_1791472781004.jpg'
    },
    {
        'title': 'Hampi Ruins Puzzle',
        'category_name': 'Architecture',
        'state_name': 'Karnataka',
        'desc': 'The ancient ruins of Vijayanagara.',
        'image': 'hampi_1791472757322.jpg'
    },
    {
        'title': 'Traditional Folklore',
        'category_name': 'Tradition',
        'state_name': 'Punjab',
        'desc': 'A depiction of traditional Punjabi folklore.',
        'image': 'uploaded_media_1791562736796.png'
    },
    {
        'title': 'Ancient Manuscript',
        'category_name': 'Literature',
        'state_name': 'Bihar',
        'desc': 'A page from an ancient Buddhist text.',
        'image': 'uploaded_media_1791563258975.png'
    },
    {
        'title': 'Folk Story Illustration',
        'category_name': 'Story',
        'state_name': 'Odisha',
        'desc': 'An illustration from a famous regional story.',
        'image': 'uploaded_media_1791566075533.png'
    }
]

# Rename .img to .png in artifacts if needed
import glob
for img_path in glob.glob(os.path.join(artifact_dir, '.user_uploaded', '*.img')):
    new_name = img_path.replace('.img', '.png')
    if not os.path.exists(new_name):
        shutil.copy(img_path, new_name)

print("Starting to seed detailed puzzles...")
for p in puzzles_to_create:
    state = State.objects.filter(name__icontains=p['state_name']).first()
    if not state:
        state = State.objects.first()
        
    category = CulturalCategory.objects.filter(name__icontains=p['category_name']).first()
    if not category:
        category = CulturalCategory.objects.first()
        
    slug = f"{p['title'].lower().replace(' ', '-')}-puzzle"
    
    # Try to copy the image
    src1 = os.path.join(artifact_dir, p['image'])
    src2 = os.path.join(artifact_dir, '.user_uploaded', p['image'])
    if os.path.exists(src1):
        shutil.copy(src1, os.path.join(media_dir, p['image']))
    elif os.path.exists(src2):
        shutil.copy(src2, os.path.join(media_dir, p['image']))
        
    Game.objects.create(
        title=p['title'],
        slug=slug,
        game_type='picture_puzzle',
        description=p['desc'],
        state=state,
        category=category,
        thumbnail=f"games/{p['image']}"
    )
    print(f"Created puzzle: {p['title']}")

print("Done seeding better puzzles!")
