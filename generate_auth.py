import os

BASE_DIR = '/Users/sapnarai/BharatVerse'

accounts_views = """from django.shortcuts import render, redirect
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
        
        # Security: Do not allow curator role in normal registration
        if role not in ['explorer', 'contributor']:
            role = 'explorer'
            
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
            
        user = UserProfile.objects.create_user(username=username, email=email, password=password, role=role)
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
"""

accounts_urls = """from django.urls import path
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
"""

core_views = """from django.shortcuts import render
from culture.models import CulturalEntry

def home(request):
    featured_entries = CulturalEntry.objects.filter(status='published')[:3]
    regions = ['North India', 'South India', 'East India', 'West India', 'Central India', 'Northeast India']
    return render(request, 'home.html', {
        'featured_entries': featured_entries,
        'regions': regions,
    })
"""

bharatverse_urls = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('api/', include('culture.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""

auth_templates = {
    'login.html': """{% extends 'base.html' %}
{% block title %}Login - BharatVerse{% endblock %}
{% block content %}
<div class="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8 border border-gray-100">
        <div>
            <h2 class="mt-2 text-center text-3xl font-extrabold text-bharat-navy font-serif">Sign in</h2>
            <p class="mt-2 text-center text-sm text-gray-600">to continue your cultural journey</p>
        </div>
        <form class="mt-8 space-y-6" action="{% url 'login' %}" method="POST">
            {% csrf_token %}
            <div class="rounded-md shadow-sm -space-y-px">
                <div class="mb-4">
                    <label for="username" class="sr-only">Username</label>
                    <input id="username" name="username" type="text" required class="appearance-none rounded-t-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-bharat-saffron focus:border-bharat-saffron focus:z-10 sm:text-sm" placeholder="Username">
                </div>
                <div>
                    <label for="password" class="sr-only">Password</label>
                    <input id="password" name="password" type="password" required class="appearance-none rounded-b-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-bharat-saffron focus:border-bharat-saffron focus:z-10 sm:text-sm" placeholder="Password">
                </div>
            </div>
            <div>
                <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-bharat-saffron hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-bharat-saffron transition">
                    Sign in
                </button>
            </div>
            <div class="text-sm text-center">
                <a href="{% url 'register' %}" class="font-medium text-bharat-amber hover:text-yellow-600">Don't have an account? Register</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
""",
    'register.html': """{% extends 'base.html' %}
{% block title %}Register - BharatVerse{% endblock %}
{% block content %}
<div class="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8 border border-gray-100">
        <div>
            <h2 class="mt-2 text-center text-3xl font-extrabold text-bharat-navy font-serif">Create Account</h2>
            <p class="mt-2 text-center text-sm text-gray-600">Join the digital cultural ecosystem</p>
        </div>
        <form class="mt-8 space-y-6" action="{% url 'register' %}" method="POST">
            {% csrf_token %}
            <div class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                    <input id="username" name="username" type="text" required class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-bharat-saffron focus:border-bharat-saffron sm:text-sm">
                </div>
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
                    <input id="email" name="email" type="email" required class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-bharat-saffron focus:border-bharat-saffron sm:text-sm">
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                    <input id="password" name="password" type="password" required class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-bharat-saffron focus:border-bharat-saffron sm:text-sm">
                </div>
                <div>
                    <label for="role" class="block text-sm font-medium text-gray-700">Join as</label>
                    <select id="role" name="role" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-bharat-saffron focus:border-bharat-saffron sm:text-sm rounded-md">
                        <option value="explorer">Explorer (Discover & Learn)</option>
                        <option value="contributor">Contributor (Submit Cultural Stories)</option>
                    </select>
                </div>
            </div>
            <div>
                <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-bharat-saffron hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-bharat-saffron transition">
                    Register
                </button>
            </div>
            <div class="text-sm text-center">
                <a href="{% url 'login' %}" class="font-medium text-bharat-amber hover:text-yellow-600">Already have an account? Sign in</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""
}

files = {
    'accounts/views.py': accounts_views,
    'accounts/urls.py': accounts_urls,
    'bharatverse/views.py': core_views,
    'bharatverse/urls.py': bharatverse_urls,
    'templates/accounts/login.html': auth_templates['login.html'],
    'templates/accounts/register.html': auth_templates['register.html'],
}

for path, content in files.items():
    with open(os.path.join(BASE_DIR, path), 'w') as f:
        f.write(content)
    print(f"Generated {path}")
