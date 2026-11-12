import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import State, CulturalCategory, CulturalEntry, CulturalMedia
from quizzes.models import Quiz, Question, QuizOption
from games.models import Game
from django.contrib.auth import get_user_model

User = get_user_model()

def seed_data():
    print("Seeding multimedia and games...")
    
    # 1. Seed some Multimedia for existing Cultural Entries
    entries = CulturalEntry.objects.filter(status='published')
    for entry in entries:
        # Avoid creating duplicates if run multiple times
        if not entry.media_items.exists():
            print(f"Adding media to {entry.title}")
            CulturalMedia.objects.create(
                cultural_entry=entry,
                title=f"Beautiful Image of {entry.title}",
                media_type='image',
                external_url='https://images.unsplash.com/photo-1599839619722-39751411ea63?q=80&w=2940&auto=format&fit=crop',
                attribution='Unsplash',
                display_order=1
            )
            CulturalMedia.objects.create(
                cultural_entry=entry,
                title=f"Experience {entry.title}",
                media_type='video',
                external_url='https://www.youtube.com/embed/Z0Xk1D4oQcE?si=B5q9x0c5_yZ8_sJ_',
                attribution='YouTube',
                display_order=2
            )

    # 2. Seed Games
    if not Game.objects.exists():
        state = State.objects.first()
        category = CulturalCategory.objects.first()
        
        # Match the Culture
        print("Creating Match the Culture game...")
        quiz1 = Quiz.objects.create(title="Match the Region", slug="match-region-demo", description="Test your knowledge of regions.", difficulty="easy")
        q1 = Question.objects.create(quiz=quiz1, question_text="Which region is famous for Bhangra?", question_type="mcq", order=1)
        QuizOption.objects.create(question=q1, option_text="Punjab", is_correct=True)
        QuizOption.objects.create(question=q1, option_text="Kerala", is_correct=False)
        Game.objects.create(title="Match the Region", slug="match-region-demo", game_type="match_culture", description="Test your knowledge.", quiz=quiz1, state=state)

        # Guess the Dance
        print("Creating Guess the Dance game...")
        quiz2 = Quiz.objects.create(title="Guess the Dance form", slug="guess-dance-demo", description="Identify the dance.", difficulty="medium")
        q2 = Question.objects.create(quiz=quiz2, question_text="Identify this famous dance form:", question_type="image", media_url="https://images.unsplash.com/photo-1599839619722-39751411ea63?q=80&w=2940", order=1)
        QuizOption.objects.create(question=q2, option_text="Kathak", is_correct=True)
        QuizOption.objects.create(question=q2, option_text="Odissi", is_correct=False)
        Game.objects.create(title="Guess the Dance form", slug="guess-dance-demo", game_type="guess_dance", description="Identify the dance.", quiz=quiz2, state=state)

        # Sound of India
        print("Creating Sound of India game...")
        quiz3 = Quiz.objects.create(title="Identify the Instrument", slug="sound-india-demo", description="Listen to the audio.", difficulty="hard")
        q3 = Question.objects.create(quiz=quiz3, question_text="Which instrument is this?", question_type="audio", media_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", order=1)
        QuizOption.objects.create(question=q3, option_text="Sitar", is_correct=True)
        QuizOption.objects.create(question=q3, option_text="Tabla", is_correct=False)
        Game.objects.create(title="Identify the Instrument", slug="sound-india-demo", game_type="sound_india", description="Listen to the audio.", quiz=quiz3, state=state)
        
    print("Done!")

if __name__ == '__main__':
    seed_data()
