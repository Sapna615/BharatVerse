import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import State, CulturalCategory, CulturalEntry, Festival, Cuisine
from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create Punjab
punjab, _ = State.objects.get_or_create(
    slug='punjab',
    defaults={
        'name': 'Punjab',
        'region': 'North India',
        'description': 'The land of five rivers, known for its rich agriculture, vibrant culture, and spirited people.',
        'cultural_summary': 'Punjab is the heart of North Indian culture, boasting energetic dances like Bhangra, rich culinary traditions, and profound spiritual heritage.'
    }
)

admin = User.objects.filter(is_superuser=True).first()

# Categories
dance, _ = CulturalCategory.objects.get_or_create(name='Dance', slug='dance')
music, _ = CulturalCategory.objects.get_or_create(name='Music', slug='music')
craft, _ = CulturalCategory.objects.get_or_create(name='Craft', slug='craft')
story, _ = CulturalCategory.objects.get_or_create(name='Story', slug='story')

# Helper function to create entries
def create_entry(title, category, short_desc, detailed):
    slug = title.lower().replace(' ', '-')
    entry, created = CulturalEntry.objects.get_or_create(
        slug=slug,
        defaults={
            'title': title,
            'category': category,
            'state': punjab,
            'short_description': short_desc,
            'detailed_story': detailed,
            'cultural_significance': 'Very significant to Punjab.',
            'practice_description': 'Practiced traditionally.',
            'status': 'published',
            'created_by': admin,
        }
    )
    if not created:
        entry.short_description = short_desc
        entry.detailed_story = detailed
        entry.save()

# --- Dance Entries ---
create_entry(
    'Bhangra', dance,
    'A high-energy, vibrant folk dance originating in the Majha area of Punjab, celebrating the harvest season.',
    'Bhangra was primarily a harvest festival dance, but has since evolved into a highly popularized cultural phenomenon globally.'
)
create_entry(
    'Giddha', dance,
    'A popular folk dance of women in Punjab, exhibiting teasing, fun, and exuberance through graceful movements.',
    'Giddha is accompanied by rhythmic clapping and the singing of traditional folk songs known as boliyan.'
)
create_entry(
    'Kikli', dance,
    'A joyful dance performed by young girls, holding hands and spinning rapidly in pairs.',
    'Kikli is a playful dance that promotes camaraderie among young women in rural Punjab.'
)

# --- Music Entries ---
create_entry(
    'Tumbi', music,
    'A traditional North Indian musical instrument from Punjab, famous for its high-pitched, single-string sound.',
    'The tumbi was popularized in modern times by Punjabi folk singers and is essential to Bhangra music.'
)
create_entry(
    'Dhol', music,
    'A large double-headed drum that provides the driving heartbeat of Punjabi folk music and dance.',
    'The powerful beat of the dhol is central to every Punjabi celebration, from weddings to harvest festivals.'
)
create_entry(
    'Algoza', music,
    'A pair of woodwind instruments used by Sindhi, Rajasthani and Punjabi folk musicians.',
    'Played using continuous breathing, the algoza provides a hypnotic drone and melody in traditional Punjabi music.'
)

# --- Craft Entries ---
create_entry(
    'Phulkari', craft,
    'Traditional embroidery from Punjab meaning "flower work", characterized by vibrant colors and intricate geometric patterns.',
    'Phulkari is deeply intertwined with the life of a Punjabi woman, historically embroidered for weddings and special occasions.'
)
create_entry(
    'Punjabi Jutti', craft,
    'Handcrafted leather footwear featuring intricate embroidery with real gold and silver threads.',
    'Punjabi juttis are known worldwide for their beautiful craftsmanship and are a staple of traditional attire.'
)
create_entry(
    'Woodwork of Hoshiarpur', craft,
    'Exquisite wooden furniture and artifacts featuring detailed brass and copper inlay work.',
    'The artisans of Hoshiarpur have preserved this intricate inlay technique for generations.'
)

# --- Story Entries ---
create_entry(
    'Heer Ranjha', story,
    'One of the most famous tragic romances of Punjab, symbolizing eternal love and devotion.',
    'Written by Waris Shah, the epic poem of Heer Ranjha is a foundational piece of Punjabi literature.'
)
create_entry(
    'Mirza Sahiban', story,
    'A popular tragic romance from Punjabi folklore, highlighting themes of love, honor, and betrayal.',
    'The story of Mirza and Sahiban is sung in traditional folk gatherings and remains a culturally significant tale.'
)

# --- Festivals ---
Festival.objects.get_or_create(
    slug='baisakhi',
    defaults={
        'name': 'Baisakhi',
        'state': punjab,
        'month': 'April',
        'description': 'A major harvest festival celebrating the solar new year and the founding of the Khalsa panth.',
        'cultural_significance': 'Highly significant for farmers and the Sikh community.'
    }
)
Festival.objects.get_or_create(
    slug='lohri',
    defaults={
        'name': 'Lohri',
        'state': punjab,
        'month': 'January',
        'description': 'A popular winter folk festival celebrated primarily in the Punjab region.',
        'cultural_significance': 'Marks the passing of the winter solstice and the arrival of longer days.'
    }
)
Festival.objects.get_or_create(
    slug='maghi',
    defaults={
        'name': 'Maghi',
        'state': punjab,
        'month': 'January',
        'description': 'The Punjabi festival of Maghi marks the changing of the season and is celebrated with bonfires and feasts.',
        'cultural_significance': 'Cultural gathering marking warmer days.'
    }
)

# --- Cuisines ---
Cuisine.objects.get_or_create(
    slug='makki-di-roti',
    defaults={
        'name': 'Makki di Roti & Sarson da Saag',
        'state': punjab,
        'description': 'A traditional winter dish made of corn flour bread and mustard greens.',
        'ingredients': 'Corn flour, mustard greens, spices, butter.',
        'cultural_context': 'The quintessential winter comfort food of rural Punjab.'
    }
)
Cuisine.objects.get_or_create(
    slug='amritsari-kulcha',
    defaults={
        'name': 'Amritsari Kulcha',
        'state': punjab,
        'description': 'A crisp, flaky bread stuffed with spiced potatoes and baked in a tandoor.',
        'ingredients': 'Flour, potatoes, spices, butter.',
        'cultural_context': 'A famous street food from Amritsar.'
    }
)
Cuisine.objects.get_or_create(
    slug='lassi',
    defaults={
        'name': 'Punjabi Lassi',
        'state': punjab,
        'description': 'A rich, creamy, yogurt-based drink served in tall brass glasses.',
        'ingredients': 'Yogurt, sugar, cream.',
        'cultural_context': 'A refreshing staple drink accompanying heavy Punjabi meals.'
    }
)

print("Punjab content seeded successfully!")
