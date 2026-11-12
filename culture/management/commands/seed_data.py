from django.core.management.base import BaseCommand
from accounts.models import UserProfile
from culture.models import State, CulturalCategory, CulturalEntry, Festival, Tradition, FolkArt, Cuisine, CulturalConnection, CulturalCalendarEvent
from gamification.models import Quest, Achievement
from quizzes.models import Quiz, Question, QuizOption
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed the database with initial cultural data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        State.objects.all().delete()
        CulturalCategory.objects.all().delete()
        CulturalEntry.objects.all().delete()
        UserProfile.objects.filter(username='admin').delete()
        
        # Create admin user
        UserProfile.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role='curator')
        
        self.stdout.write('Creating Categories...')
        categories = ['Dance', 'Music', 'Festival', 'Art', 'Craft', 'Cuisine', 'Clothing', 'Architecture', 'Tradition', 'Story', 'Literature']
        cat_objs = {}
        for c in categories:
            cat_objs[c] = CulturalCategory.objects.create(name=c, slug=slugify(c), description=f'Category for {c}')
            
        self.stdout.write('Creating States (20+)...')
        states_data = [
            ('Punjab', 'North India'), ('Rajasthan', 'North India'), ('Kerala', 'South India'), 
            ('Tamil Nadu', 'South India'), ('Gujarat', 'West India'), ('Maharashtra', 'West India'),
            ('West Bengal', 'East India'), ('Odisha', 'East India'), ('Assam', 'Northeast India'),
            ('Manipur', 'Northeast India'), ('Karnataka', 'South India'), ('Andhra Pradesh', 'South India'),
            ('Telangana', 'South India'), ('Uttar Pradesh', 'North India'), ('Madhya Pradesh', 'Central India'),
            ('Chhattisgarh', 'Central India'), ('Bihar', 'East India'), ('Jharkhand', 'East India'),
            ('Himachal Pradesh', 'North India'), ('Uttarakhand', 'North India'), ('Haryana', 'North India'),
            ('Sikkim', 'Northeast India')
        ]
        state_objs = {}
        for name, region in states_data:
            state_objs[name] = State.objects.create(
                name=name, slug=slugify(name), region=region, description=f'Rich culture of {name}', cultural_summary='Summary'
            )
            
        self.stdout.write('Creating Cultural Entries, Festivals, Traditions, Folk Arts, Cuisines...')
        
        # We will iterate and create many entries to reach the required count
        # 50 entries, 20 festivals, 20 traditions, 15 folk arts, 15 cuisines
        
        for state_name, state in state_objs.items():
            # 1 Festival per state (20 total)
            f = Festival.objects.create(
                name=f"{state_name} Festival", slug=slugify(f"{state_name} Festival"), state=state,
                month="January", description=f"A popular festival in {state_name}.",
                cultural_significance="Important cultural celebration."
            )
            
            # 1 Tradition per state (20 total)
            Tradition.objects.create(
                name=f"{state_name} Tradition", slug=slugify(f"{state_name} Tradition"), state=state,
                description=f"A long standing tradition in {state_name}.", story="An old story about it."
            )
            
            # 1 Folk Art for first 15 states
            if list(state_objs.keys()).index(state_name) < 15:
                FolkArt.objects.create(
                    name=f"{state_name} Folk Art", slug=slugify(f"{state_name} Folk Art"), state=state,
                    description="Traditional art form.", technique="Unique technique.", cultural_context="Context."
                )
                
            # 1 Cuisine for first 15 states
            if list(state_objs.keys()).index(state_name) < 15:
                Cuisine.objects.create(
                    name=f"{state_name} Cuisine", slug=slugify(f"{state_name} Cuisine"), state=state,
                    description="Delicious food.", ingredients="Spices, herbs.", cultural_context="Daily staple."
                )
                
            # Create a few cultural entries per state to reach >50
            CulturalEntry.objects.create(
                title=f"{state_name} Dance Entry", slug=slugify(f"{state_name} Dance Entry"),
                category=cat_objs['Dance'], state=state, short_description="A folk dance.",
                detailed_story="Detailed story of the dance.", cultural_significance="Very significant.",
                practice_description="Danced in groups.", status='published'
            )
            CulturalEntry.objects.create(
                title=f"{state_name} Craft Entry", slug=slugify(f"{state_name} Craft Entry"),
                category=cat_objs['Craft'], state=state, short_description="A folk craft.",
                detailed_story="Detailed story of the craft.", cultural_significance="Very significant.",
                practice_description="Made by artisans.", status='published'
            )
            CulturalEntry.objects.create(
                title=f"{state_name} Music Entry", slug=slugify(f"{state_name} Music Entry"),
                category=cat_objs['Music'], state=state, short_description="A folk music style.",
                detailed_story="Detailed story of the music.", cultural_significance="Very significant.",
                practice_description="Sung in groups.", status='published'
            )

        self.stdout.write('Creating Cultural Connections (20+)...')
        all_entries = list(CulturalEntry.objects.all())
        for i in range(20):
            source = all_entries[i]
            target = all_entries[(i + 1) % len(all_entries)]
            if source != target:
                CulturalConnection.objects.get_or_create(
                    source_entry=source, target_entry=target,
                    relationship_type='shares_origin_with', description='They share cultural roots.'
                )
                
        self.stdout.write('Creating Quizzes and Questions (20+)...')
        q = Quiz.objects.create(title="India Cultural Quiz", slug="india-cultural-quiz", description="Test your knowledge", difficulty="easy")
        for i in range(20):
            qst = Question.objects.create(quiz=q, question_text=f"Sample Question {i+1}?", points=10)
            QuizOption.objects.create(question=qst, option_text="Option A", is_correct=True)
            QuizOption.objects.create(question=qst, option_text="Option B", is_correct=False)
            
        self.stdout.write('Creating Quests and Achievements (10+)...')
        for i in range(10):
            Quest.objects.create(title=f"Quest {i+1}", slug=slugify(f"Quest {i+1}"), description="Complete this quest", requirement=f"Explore {i} places", xp=50)
            Achievement.objects.create(name=f"Achievement {i+1}", slug=slugify(f"Achievement {i+1}"), description="Unlock this", xp_reward=100)
            
        self.stdout.write('Creating Calendar Events (10+)...')
        for i in range(10):
            CulturalCalendarEvent.objects.create(
                name=f"Event {i+1}", slug=slugify(f"Event {i+1}"), month="January", description="An event."
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
