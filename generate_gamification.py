import os

BASE_DIR = '/Users/sapnarai/BharatVerse'

# 1. Update Gamification Models
gamification_models_addition = """
class XPTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_transactions')
    amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    source_type = models.CharField(max_length=100, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} | {self.amount} XP | {self.reason}"
"""
with open(os.path.join(BASE_DIR, 'gamification', 'models.py'), 'a') as f:
    f.write(gamification_models_addition)

# 2. Gamification Services
gamification_services = """from .models import XPTransaction, Achievement, UserAchievement, Quest
from quizzes.models import QuizAttempt

def award_xp(user, amount, reason, source_type=None, source_id=None):
    # Prevent duplicate transaction for same source if provided
    if source_type and source_id:
        if XPTransaction.objects.filter(user=user, source_type=source_type, source_id=source_id).exists():
            return False
            
    XPTransaction.objects.create(
        user=user, amount=amount, reason=reason,
        source_type=source_type, source_id=source_id
    )
    user.xp += amount
    user.save()
    check_and_unlock_achievements(user)
    return True

def check_and_unlock_achievements(user):
    unlocked = []
    
    # 1. BharatVerse Scholar
    if user.xp >= 1000:
        ach, _ = Achievement.objects.get_or_create(name='BharatVerse Scholar', defaults={'slug': 'scholar', 'xp_reward': 200, 'description': 'Reach 1000 XP.'})
        if not UserAchievement.objects.filter(user=user, achievement=ach).exists():
            UserAchievement.objects.create(user=user, achievement=ach)
            award_xp(user, ach.xp_reward, 'Unlocked BharatVerse Scholar')
            unlocked.append(ach)

    # 2. Quiz Starter
    if QuizAttempt.objects.filter(user=user).exists():
        ach, _ = Achievement.objects.get_or_create(name='Quiz Starter', defaults={'slug': 'quiz-starter', 'xp_reward': 50, 'description': 'Complete your first quiz.'})
        if not UserAchievement.objects.filter(user=user, achievement=ach).exists():
            UserAchievement.objects.create(user=user, achievement=ach)
            award_xp(user, ach.xp_reward, 'Unlocked Quiz Starter')
            unlocked.append(ach)
            
    # 3. Quiz Master
    if QuizAttempt.objects.filter(user=user, percentage__gte=90).exists():
        ach, _ = Achievement.objects.get_or_create(name='Quiz Master', defaults={'slug': 'quiz-master', 'xp_reward': 100, 'description': 'Score 90%+ on a quiz.'})
        if not UserAchievement.objects.filter(user=user, achievement=ach).exists():
            UserAchievement.objects.create(user=user, achievement=ach)
            award_xp(user, ach.xp_reward, 'Unlocked Quiz Master')
            unlocked.append(ach)
            
    return unlocked

def get_quest_progress(user, quest):
    # dynamic logic based on quest type
    # For now, simplistic
    if 'quiz' in quest.title.lower():
        current = QuizAttempt.objects.filter(user=user).count()
        target = 3
    else:
        current = 1
        target = 5
        
    return {
        'current': current,
        'target': target,
        'percentage': min(100, int((current/target)*100)),
        'completed': current >= target
    }
"""
with open(os.path.join(BASE_DIR, 'gamification', 'services.py'), 'w') as f:
    f.write(gamification_services)

# 3. Gamification Views & URLs
gamification_views = """from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quest, Achievement, UserAchievement, XPTransaction
from .services import get_quest_progress

@login_required
def dashboard(request):
    transactions = XPTransaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    achievements = UserAchievement.objects.filter(user=request.user).order_by('-earned_at')[:5]
    
    # Calculate Level
    xp = request.user.xp
    if xp < 100: level = "Curious Explorer"
    elif xp < 250: level = "Culture Seeker"
    elif xp < 500: level = "Heritage Explorer"
    elif xp < 1000: level = "Tradition Keeper"
    else: level = "BharatVerse Scholar"
    
    return render(request, 'gamification/dashboard.html', {
        'transactions': transactions,
        'achievements': achievements,
        'level_name': level,
    })

@login_required
def quests_list(request):
    quests = Quest.objects.filter(is_active=True)
    quest_data = []
    for q in quests:
        prog = get_quest_progress(request.user, q)
        quest_data.append({'quest': q, 'progress': prog})
        
    return render(request, 'gamification/quests.html', {'quest_data': quest_data})

@login_required
def achievements_list(request):
    all_achievements = Achievement.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True)
    return render(request, 'gamification/achievements.html', {
        'achievements': all_achievements,
        'user_achievements': user_achievements
    })
"""
with open(os.path.join(BASE_DIR, 'gamification', 'views.py'), 'w') as f:
    f.write(gamification_views)

gamification_urls = """from django.urls import path
from .views import dashboard, quests_list, achievements_list

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('quests/', quests_list, name='quests_list'),
    path('achievements/', achievements_list, name='achievements_list'),
]
"""
with open(os.path.join(BASE_DIR, 'gamification', 'urls.py'), 'w') as f:
    f.write(gamification_urls)


# 4. Quizzes Views & URLs
quizzes_views = """from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, Question, QuizOption, QuizAttempt
from gamification.services import award_xp

def quiz_list(request):
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug, is_active=True)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})

@login_required
def take_quiz(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug, is_active=True)
    questions = quiz.questions.all().order_by('order')
    
    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        for q in questions:
            selected_option = request.POST.get(f'q_{q.id}')
            if selected_option:
                opt = get_object_or_404(QuizOption, id=selected_option, question=q)
                if opt.is_correct:
                    score += 1
                    
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        attempt = QuizAttempt.objects.create(
            user=request.user, quiz=quiz, score=score, 
            total_questions=total_questions, percentage=percentage
        )
        
        # Award XP
        base_xp = 20
        bonus = 0
        if percentage >= 90: bonus = 30
        elif percentage >= 70: bonus = 20
        elif percentage >= 50: bonus = 10
        else: bonus = 5
        
        award_xp(request.user, base_xp + bonus, f'Completed {quiz.title} ({int(percentage)}%)', 'quiz_attempt', attempt.id)
        
        return redirect('quiz_result', attempt_id=attempt.id)
        
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    return render(request, 'quizzes/quiz_result.html', {'attempt': attempt})
"""
with open(os.path.join(BASE_DIR, 'quizzes', 'views.py'), 'w') as f:
    f.write(quizzes_views)

quizzes_urls = """from django.urls import path
from .views import quiz_list, quiz_detail, take_quiz, quiz_result

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<slug:slug>/', quiz_detail, name='quiz_detail'),
    path('<slug:slug>/take/', take_quiz, name='take_quiz'),
    path('result/<int:attempt_id>/', quiz_result, name='quiz_result'),
]
"""
with open(os.path.join(BASE_DIR, 'quizzes', 'urls.py'), 'w') as f:
    f.write(quizzes_urls)

# 5. Connect to bharatverse/urls.py
with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'r') as f:
    bv_urls = f.read()

if "'quizzes.urls'" not in bv_urls:
    bv_urls = bv_urls.replace(
        "path('api/', include('culture.urls')),",
        "path('api/', include('culture.urls')),\n    path('quizzes/', include('quizzes.urls')),\n    path('gamification/', include('gamification.urls')),"
    )
    with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'w') as f:
        f.write(bv_urls)

# 6. Templates Generation
templates = {
    'quizzes/quiz_list.html': """{% extends 'base.html' %}
{% block title %}Cultural Quizzes - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">Test Your Cultural Knowledge</h1>
    <p class="text-gray-300 font-light">Learn something new. Challenge yourself. Discover more about India.</p>
</div>
<div class="max-w-7xl mx-auto px-4 py-16 grid grid-cols-1 md:grid-cols-3 gap-8">
    {% for q in quizzes %}
    <div class="bg-white rounded-xl shadow p-6 border border-gray-100 flex flex-col h-full">
        <h3 class="text-xl font-bold text-bharat-navy mb-2">{{ q.title }}</h3>
        <p class="text-sm text-gray-600 flex-grow mb-4">{{ q.description }}</p>
        <div class="flex justify-between items-center mb-6 text-sm font-bold text-gray-500">
            <span>{{ q.questions.count }} Questions</span>
            <span class="text-bharat-saffron uppercase">{{ q.difficulty }}</span>
        </div>
        <a href="{% url 'quiz_detail' q.slug %}" class="block text-center bg-bharat-saffron text-white font-bold py-2 rounded shadow hover:bg-orange-600 transition">Start Quiz</a>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    'quizzes/take_quiz.html': """{% extends 'base.html' %}
{% block title %}Taking: {{ quiz.title }}{% endblock %}
{% block content %}
<div class="max-w-3xl mx-auto px-4 py-16">
    <h1 class="text-3xl font-serif font-bold text-bharat-navy mb-8 text-center">{{ quiz.title }}</h1>
    <form method="POST" action="{% url 'take_quiz' quiz.slug %}" class="space-y-12">
        {% csrf_token %}
        {% for q in questions %}
        <div class="bg-white rounded-xl shadow p-8 border border-gray-100">
            <h3 class="text-lg font-bold text-gray-800 mb-6">{{ forloop.counter }}. {{ q.question_text }}</h3>
            <div class="space-y-4">
                {% for opt in q.options.all %}
                <label class="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition">
                    <input type="radio" name="q_{{ q.id }}" value="{{ opt.id }}" required class="h-4 w-4 text-bharat-saffron focus:ring-bharat-saffron">
                    <span class="text-gray-700">{{ opt.option_text }}</span>
                </label>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
        <div class="text-center">
            <button type="submit" class="bg-bharat-navy text-white font-bold py-4 px-12 rounded-full shadow hover:bg-gray-800 transition text-lg">Submit Quiz</button>
        </div>
    </form>
</div>
{% endblock %}""",

    'quizzes/quiz_result.html': """{% extends 'base.html' %}
{% block title %}Quiz Complete!{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto px-4 py-16 text-center">
    <h1 class="text-5xl font-serif font-bold text-green-600 mb-4">Quiz Complete! 🎉</h1>
    <p class="text-xl text-gray-600 mb-8">{{ attempt.quiz.title }}</p>
    
    <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-12 mb-8">
        <div class="text-6xl font-black text-bharat-navy mb-4">{{ attempt.score }} <span class="text-2xl text-gray-400">/ {{ attempt.total_questions }}</span></div>
        <div class="text-2xl font-bold text-bharat-saffron">{{ attempt.percentage|floatformat:0 }}%</div>
    </div>
    
    <div class="flex flex-col sm:flex-row justify-center gap-4">
        <a href="{% url 'take_quiz' attempt.quiz.slug %}" class="bg-gray-200 text-bharat-navy font-bold py-3 px-8 rounded-full shadow hover:bg-gray-300">Try Again</a>
        <a href="{% url 'quiz_list' %}" class="bg-bharat-saffron text-white font-bold py-3 px-8 rounded-full shadow hover:bg-orange-600">Back to Quizzes</a>
    </div>
</div>
{% endblock %}""",

    'gamification/dashboard.html': """{% extends 'base.html' %}
{% block title %}Gamification Dashboard{% endblock %}
{% block content %}
<div class="max-w-5xl mx-auto px-4 py-16">
    <div class="bg-bharat-navy rounded-2xl shadow p-8 text-center text-white mb-12">
        <h1 class="text-4xl font-serif font-bold mb-2">Your Cultural Progress</h1>
        <p class="text-bharat-saffron font-bold uppercase tracking-widest text-sm mb-6">{{ level_name }}</p>
        <div class="text-5xl font-black mb-4">{{ user.xp }} <span class="text-xl text-gray-400 font-normal">XP</span></div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 class="text-xl font-bold text-bharat-navy mb-4">Recent XP Activity</h3>
            <div class="space-y-4">
                {% for tx in transactions %}
                <div class="flex justify-between items-center pb-2 border-b border-gray-50">
                    <span class="text-sm text-gray-600">{{ tx.reason }}</span>
                    <span class="text-sm font-bold text-green-600">+{{ tx.amount }} XP</span>
                </div>
                {% empty %}
                <p class="text-sm text-gray-500 italic">No XP activity yet.</p>
                {% endfor %}
            </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 class="text-xl font-bold text-bharat-navy mb-4">Recent Achievements</h3>
            <div class="space-y-4">
                {% for a in achievements %}
                <div class="flex items-center gap-4 bg-gray-50 p-3 rounded">
                    <div class="w-10 h-10 rounded-full bg-bharat-amber flex items-center justify-center text-white text-lg font-bold shadow">🏆</div>
                    <div>
                        <div class="font-bold text-bharat-navy text-sm">{{ a.achievement.name }}</div>
                        <div class="text-xs text-gray-500">{{ a.achievement.description }}</div>
                    </div>
                </div>
                {% empty %}
                <p class="text-sm text-gray-500 italic">No achievements unlocked yet.</p>
                {% endfor %}
            </div>
            <a href="{% url 'achievements_list' %}" class="block mt-4 text-sm font-bold text-bharat-saffron hover:underline">View All Achievements &rarr;</a>
        </div>
    </div>
</div>
{% endblock %}""",

    'gamification/achievements.html': """{% extends 'base.html' %}
{% block title %}Achievements{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">Your Cultural Achievements</h1>
    <p class="text-gray-300 font-light">Every discovery brings you closer to India's stories.</p>
</div>
<div class="max-w-5xl mx-auto px-4 py-16 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
    {% for ach in achievements %}
    <div class="bg-white p-6 rounded-xl border {% if ach.id in user_achievements %}border-bharat-amber shadow-md{% else %}border-gray-200 opacity-60 grayscale{% endif %} text-center">
        <div class="w-16 h-16 mx-auto rounded-full bg-gradient-to-br {% if ach.id in user_achievements %}from-bharat-saffron to-bharat-amber shadow-lg{% else %}from-gray-300 to-gray-400{% endif %} flex items-center justify-center text-3xl mb-4">🏆</div>
        <h3 class="font-bold text-bharat-navy mb-1">{{ ach.name }}</h3>
        <p class="text-xs text-gray-500 mb-3">{{ ach.description }}</p>
        <span class="text-xs font-bold text-bharat-saffron bg-orange-50 px-2 py-1 rounded">{{ ach.xp_reward }} XP</span>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    'gamification/quests.html': """{% extends 'base.html' %}
{% block title %}Quests{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">Cultural Quests</h1>
    <p class="text-gray-300 font-light">Turn exploration into an adventure.</p>
</div>
<div class="max-w-4xl mx-auto px-4 py-16 space-y-6">
    {% for data in quest_data %}
    <div class="bg-white rounded-xl shadow p-6 border border-gray-100 flex flex-col md:flex-row items-center gap-6">
        <div class="flex-grow">
            <h3 class="text-xl font-bold text-bharat-navy mb-1">{{ data.quest.title }}</h3>
            <p class="text-sm text-gray-600 mb-4">{{ data.quest.requirement }}</p>
            <div class="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div class="bg-bharat-saffron h-2 rounded-full" style="width: {{ data.progress.percentage }}%"></div>
            </div>
            <div class="text-xs text-gray-500 font-bold">{{ data.progress.current }} / {{ data.progress.target }} Completed</div>
        </div>
        <div class="shrink-0 text-center">
            <div class="text-lg font-black text-bharat-amber mb-2">+{{ data.quest.xp }} XP</div>
            {% if data.progress.completed %}
            <span class="bg-green-100 text-green-700 font-bold px-4 py-2 rounded shadow-sm block">Completed</span>
            {% else %}
            <button class="bg-bharat-navy text-white font-bold px-4 py-2 rounded shadow hover:bg-gray-800 transition">Continue</button>
            {% endif %}
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}"""
}

for path, content in templates.items():
    full_path = os.path.join(BASE_DIR, 'templates', path)
    with open(full_path, 'w') as f:
        f.write(content)
    print(f"Generated {full_path}")
