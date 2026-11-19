from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        # Custom basic registration logic
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'explorer')
        
        if role not in ['explorer', 'contributor', 'curator']:
            role = 'explorer'
            
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
            
        user = UserProfile.objects.create_user(username=username, email=email, password=password, role=role)
        if role == 'curator':
            user.is_staff = True
            user.save()
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to BharatVerse.')
        return redirect('home')
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')

def direct_reset_password(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not identifier or not new_password:
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/reset_password_direct.html')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_direct.html')

        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_direct.html')

        # Find user by username or email
        user = UserProfile.objects.filter(username__iexact=identifier).first() or \
               UserProfile.objects.filter(email__iexact=identifier).first()

        if user:
            user.set_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, f'Password successfully updated! Welcome back, {user.username}.')
            return redirect('home')
        else:
            messages.error(request, 'No account found with that username or email.')
            return render(request, 'accounts/reset_password_direct.html')

    return render(request, 'accounts/reset_password_direct.html')

from django.contrib.auth.decorators import login_required
from quizzes.models import QuizAttempt
from journeys.models import CulturalJourney
from contributions.models import Submission

@login_required(login_url='/accounts/login/')
def profile_view(request):
    user = request.user
    quiz_attempts = QuizAttempt.objects.filter(user=user).select_related('quiz').order_by('-completed_at')[:5]
    journeys = CulturalJourney.objects.filter(user=user).order_by('-created_at')[:5]
    submissions = Submission.objects.filter(contributor=user).order_by('-created_at')[:5] if user.role in ['contributor', 'curator'] or user.is_superuser else []

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        region = request.POST.get('region', '')
        user.bio = bio
        user.region = region
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Your profile details have been updated.')
        return redirect('profile')

    context = {
        'profile_user': user,
        'quiz_attempts': quiz_attempts,
        'journeys': journeys,
        'submissions': submissions,
        'total_quizzes': QuizAttempt.objects.filter(user=user).count(),
        'total_journeys': CulturalJourney.objects.filter(user=user).count(),
    }
    return render(request, 'accounts/profile.html', context)
