from django.shortcuts import render, get_object_or_404, redirect
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
    
    if request.method == 'POST':
        score = 0
        total_questions = 0
        for key, selected_option in request.POST.items():
            if key.startswith('q_'):
                total_questions += 1
                opt = get_object_or_404(QuizOption, id=selected_option)
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
        
    # GET request: shuffle questions and limit to 5
    questions = quiz.questions.all().order_by('?')[:5]
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    return render(request, 'quizzes/quiz_result.html', {'attempt': attempt})
