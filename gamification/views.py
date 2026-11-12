from django.shortcuts import render, redirect
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
