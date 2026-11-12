from .models import XPTransaction, Achievement, UserAchievement, Quest
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
