import os

BASE_DIR = '/Users/sapnarai/BharatVerse'

# 1. Update exploration/views.py to include compare and favorites
exploration_views_addition = """
def compare_cultures(request):
    state1_id = request.GET.get('state1')
    state2_id = request.GET.get('state2')
    
    context = {'states': State.objects.all().order_by('name')}
    
    if state1_id and state2_id and state1_id != state2_id:
        s1 = get_object_or_404(State, id=state1_id)
        s2 = get_object_or_404(State, id=state2_id)
        
        # Calculate fingerprint for s1
        entries1 = CulturalEntry.objects.filter(state=s1, status='published')
        s1_fp = {
            'Dance': entries1.filter(category__name__iexact='Dance').count(),
            'Music': entries1.filter(category__name__iexact='Music').count(),
            'Craft': entries1.filter(category__name__iexact='Craft').count(),
            'Cuisine': Cuisine.objects.filter(state=s1).count(),
            'Festivals': Festival.objects.filter(state=s1).count(),
            'Stories': entries1.filter(category__name__iexact='Story').count(),
        }
        
        # Calculate fingerprint for s2
        entries2 = CulturalEntry.objects.filter(state=s2, status='published')
        s2_fp = {
            'Dance': entries2.filter(category__name__iexact='Dance').count(),
            'Music': entries2.filter(category__name__iexact='Music').count(),
            'Craft': entries2.filter(category__name__iexact='Craft').count(),
            'Cuisine': Cuisine.objects.filter(state=s2).count(),
            'Festivals': Festival.objects.filter(state=s2).count(),
            'Stories': entries2.filter(category__name__iexact='Story').count(),
        }
        
        context.update({
            's1': s1, 's2': s2,
            's1_fp': s1_fp, 's2_fp': s2_fp,
            'entries1': entries1[:3], 'entries2': entries2[:3]
        })
        
    return render(request, 'exploration/compare.html', context)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'exploration/favorites.html', {'favorites': favorites})
"""

# Append to exploration/views.py
with open(os.path.join(BASE_DIR, 'exploration', 'views.py'), 'a') as f:
    f.write(exploration_views_addition)

# 2. Update exploration/urls.py
exploration_urls_addition = """
    path('compare/', compare_cultures, name='compare_cultures'),
    path('favorites/', favorites_list, name='favorites_list'),
"""

# Read exploration/urls.py, insert into urlpatterns
with open(os.path.join(BASE_DIR, 'exploration', 'urls.py'), 'r') as f:
    urls_content = f.read()

urls_content = urls_content.replace(
    'from .views import (explore_india, cultural_map, state_detail, \n                    cultural_entry_detail, cultural_connections,\n                    toggle_favorite, add_to_journey)',
    'from .views import (explore_india, cultural_map, state_detail, \n                    cultural_entry_detail, cultural_connections,\n                    toggle_favorite, add_to_journey, compare_cultures, favorites_list)'
)
urls_content = urls_content.replace(']', exploration_urls_addition + ']')

with open(os.path.join(BASE_DIR, 'exploration', 'urls.py'), 'w') as f:
    f.write(urls_content)


# 3. Create Search View in bharatverse/views.py
search_views_addition = """
from django.db.models import Q
from culture.models import CulturalEntry, State, Festival, Tradition, FolkArt, Cuisine, CulturalStory

def global_search(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        entries = CulturalEntry.objects.filter(Q(title__icontains=query) | Q(short_description__icontains=query), status='published')
        states = State.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        festivals = Festival.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        stories = CulturalStory.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), moderation_status='approved')
        
        for e in entries: results.append({'type': 'Cultural Entry', 'title': e.title, 'desc': e.short_description, 'url': f'/explore/culture/{e.slug}/', 'obj': e})
        for s in states: results.append({'type': 'State', 'title': s.name, 'desc': s.description, 'url': f'/explore/states/{s.slug}/', 'obj': s})
        for f in festivals: results.append({'type': 'Festival', 'title': f.name, 'desc': f.description, 'url': '#', 'obj': f})
        for st in stories: results.append({'type': 'Story', 'title': st.title, 'desc': st.content[:100], 'url': '#', 'obj': st})
        
    return render(request, 'search.html', {'query': query, 'results': results})
"""
with open(os.path.join(BASE_DIR, 'bharatverse', 'views.py'), 'a') as f:
    f.write(search_views_addition)

# Update bharatverse/urls.py for search
with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'r') as f:
    bv_urls = f.read()

bv_urls = bv_urls.replace('from .views import home', 'from .views import home, global_search')
bv_urls = bv_urls.replace("path('', home, name='home'),", "path('', home, name='home'),\n    path('search/', global_search, name='global_search'),\n    path('journey/', include('journeys.urls')),")

with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'w') as f:
    f.write(bv_urls)


# 4. Create journeys/views.py and urls.py
journeys_views = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CulturalJourney, JourneyItem

@login_required
def my_journey(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            CulturalJourney.objects.create(user=request.user, title=title)
            messages.success(request, 'Journey created successfully.')
        return redirect('my_journey')
        
    journeys = CulturalJourney.objects.filter(user=request.user).order_by('-created_at')
    active_journey = journeys.first() if journeys.exists() else None
    items = JourneyItem.objects.filter(journey=active_journey).order_by('order') if active_journey else []
    
    # calc progress dynamically
    progress = 0
    if items:
        completed = items.filter(completed=True).count()
        progress = int((completed / items.count()) * 100)
    
    return render(request, 'journeys/my_journey.html', {
        'journeys': journeys,
        'active_journey': active_journey,
        'items': items,
        'progress': progress
    })

@login_required
def toggle_journey_item(request, item_id):
    item = get_object_or_404(JourneyItem, id=item_id, journey__user=request.user)
    item.completed = not item.completed
    item.save()
    
    if item.completed:
        request.user.xp += 10
        request.user.save()
        messages.success(request, 'Item marked complete! +10 XP')
    return redirect('my_journey')
"""
with open(os.path.join(BASE_DIR, 'journeys', 'views.py'), 'w') as f:
    f.write(journeys_views)

journeys_urls = """from django.urls import path
from .views import my_journey, toggle_journey_item

urlpatterns = [
    path('', my_journey, name='my_journey'),
    path('toggle/<int:item_id>/', toggle_journey_item, name='toggle_journey_item'),
]
"""
with open(os.path.join(BASE_DIR, 'journeys', 'urls.py'), 'w') as f:
    f.write(journeys_urls)


# 5. Templates
search_html = """{% extends 'base.html' %}
{% block title %}Search - BharatVerse{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-16">
    <form method="GET" action="{% url 'global_search' %}" class="mb-12">
        <div class="flex">
            <input type="text" name="q" value="{{ query }}" placeholder="Search India's stories, traditions, festivals, art..." class="w-full text-lg px-6 py-4 border-2 border-bharat-navy rounded-l-xl focus:outline-none focus:ring-2 focus:ring-bharat-saffron">
            <button type="submit" class="bg-bharat-navy text-white px-8 py-4 rounded-r-xl font-bold hover:bg-gray-800 transition">Search</button>
        </div>
    </form>
    
    {% if query %}
        <h2 class="text-2xl font-serif text-bharat-navy mb-8">Search Results for "{{ query }}"</h2>
        
        {% if results %}
            <div class="space-y-6">
                {% for res in results %}
                <a href="{{ res.url }}" class="block bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:border-bharat-saffron hover:shadow-md transition">
                    <span class="text-xs font-bold text-bharat-saffron uppercase tracking-wider block mb-1">{{ res.type }}</span>
                    <h3 class="text-xl font-bold text-bharat-navy mb-2">{{ res.title }}</h3>
                    <p class="text-gray-600 line-clamp-2">{{ res.desc }}</p>
                </a>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center py-16 bg-gray-50 rounded-2xl border border-gray-100">
                <h3 class="text-3xl font-serif text-bharat-navy mb-4">We couldn't find that cultural story yet.</h3>
                <p class="text-gray-600 mb-8">Try another search or explore India by region.</p>
                <a href="/explore/" class="bg-bharat-saffron text-white px-6 py-3 rounded-full font-bold shadow hover:bg-orange-600">Explore India</a>
            </div>
        {% endif %}
    {% endif %}
</div>
{% endblock %}
"""
with open(os.path.join(BASE_DIR, 'templates', 'search.html'), 'w') as f:
    f.write(search_html)

compare_html = """{% extends 'base.html' %}
{% block title %}Compare Cultures - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">Compare Cultures</h1>
    <p class="text-gray-300 font-light">Discover how different regions express India's cultural diversity.</p>
</div>

<div class="max-w-6xl mx-auto px-4 py-12">
    <form method="GET" action="{% url 'compare_cultures' %}" class="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 mb-12 flex flex-col md:flex-row gap-6 items-end justify-center">
        <div class="w-full md:w-1/3">
            <label class="block text-sm font-bold text-gray-700 mb-2">Culture A</label>
            <select name="state1" required class="w-full border-2 border-gray-200 rounded-lg p-3">
                <option value="">Select State</option>
                {% for s in states %}
                <option value="{{ s.id }}" {% if request.GET.state1 == s.id|stringformat:"s" %}selected{% endif %}>{{ s.name }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="w-full md:w-1/3">
            <label class="block text-sm font-bold text-gray-700 mb-2">Culture B</label>
            <select name="state2" required class="w-full border-2 border-gray-200 rounded-lg p-3">
                <option value="">Select State</option>
                {% for s in states %}
                <option value="{{ s.id }}" {% if request.GET.state2 == s.id|stringformat:"s" %}selected{% endif %}>{{ s.name }}</option>
                {% endfor %}
            </select>
        </div>
        <div>
            <button type="submit" class="bg-bharat-saffron text-white px-8 py-3 rounded-lg font-bold hover:bg-orange-600 h-[52px]">Compare</button>
        </div>
    </form>
    
    {% if s1 and s2 %}
    <p class="text-center text-sm text-gray-500 mb-8 italic">Comparison metrics reflect the cultural content currently available in BharatVerse and are not measurements of cultural importance or richness.</p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
        <!-- Culture A -->
        <div>
            <div class="text-center mb-8 border-b-2 border-bharat-navy pb-4">
                <h2 class="text-3xl font-serif font-bold text-bharat-navy">{{ s1.name }}</h2>
                <span class="text-bharat-saffron font-bold text-sm uppercase tracking-wider">{{ s1.region }}</span>
            </div>
            
            <div class="space-y-4 mb-12">
                {% for k, v in s1_fp.items %}
                <div class="flex justify-between items-center bg-gray-50 p-3 rounded border border-gray-100">
                    <span class="font-bold text-gray-700">{{ k }}</span>
                    <span class="bg-bharat-navy text-white text-xs px-2 py-1 rounded">{{ v }} items</span>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <!-- Culture B -->
        <div>
            <div class="text-center mb-8 border-b-2 border-bharat-saffron pb-4">
                <h2 class="text-3xl font-serif font-bold text-bharat-navy">{{ s2.name }}</h2>
                <span class="text-bharat-amber font-bold text-sm uppercase tracking-wider">{{ s2.region }}</span>
            </div>
            
            <div class="space-y-4 mb-12">
                {% for k, v in s2_fp.items %}
                <div class="flex justify-between items-center bg-gray-50 p-3 rounded border border-gray-100">
                    <span class="font-bold text-gray-700">{{ k }}</span>
                    <span class="bg-bharat-saffron text-white text-xs px-2 py-1 rounded">{{ v }} items</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
"""
with open(os.path.join(BASE_DIR, 'templates', 'exploration', 'compare.html'), 'w') as f:
    f.write(compare_html)

favorites_html = """{% extends 'base.html' %}
{% block title %}My Favorites - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">My Favorites</h1>
    <p class="text-gray-300 font-light">The cultural stories you want to return to.</p>
</div>

<div class="max-w-7xl mx-auto px-4 py-16">
    {% if favorites %}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {% for fav in favorites %}
            <div class="bg-white rounded-xl shadow-sm hover:shadow-md border border-gray-100 p-6 flex flex-col h-full">
                <span class="text-xs text-gray-500 uppercase font-bold">{{ fav.cultural_entry.category.name }}</span>
                <h3 class="text-xl font-bold text-bharat-navy mt-1 mb-2">{{ fav.cultural_entry.title }}</h3>
                <p class="text-sm text-gray-600 line-clamp-3 mb-4 flex-grow">{{ fav.cultural_entry.short_description }}</p>
                <div class="flex gap-4 mt-auto">
                    <a href="{% url 'cultural_entry_detail' fav.cultural_entry.slug %}" class="bg-gray-100 text-bharat-navy text-sm font-bold px-4 py-2 rounded-lg hover:bg-gray-200 text-center flex-grow">Open</a>
                    <form action="{% url 'toggle_favorite' fav.cultural_entry.slug %}" method="POST">
                        {% csrf_token %}
                        <button type="submit" class="bg-red-50 text-red-600 text-sm font-bold px-4 py-2 rounded-lg hover:bg-red-100">Remove</button>
                    </form>
                </div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="text-center py-20 bg-gray-50 rounded-2xl border border-gray-100 max-w-3xl mx-auto">
            <h2 class="text-3xl font-serif text-bharat-navy mb-4">Your cultural shelf is empty.</h2>
            <p class="text-gray-600 mb-8">Save traditions, stories and cultural discoveries here so you can return to them anytime.</p>
            <a href="/explore/" class="bg-bharat-saffron text-white px-8 py-3 rounded-full font-bold hover:bg-orange-600 shadow">Explore India</a>
        </div>
    {% endif %}
</div>
{% endblock %}
"""
with open(os.path.join(BASE_DIR, 'templates', 'exploration', 'favorites.html'), 'w') as f:
    f.write(favorites_html)

journey_html = """{% extends 'base.html' %}
{% block title %}My Cultural Journey - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">My Cultural Journey</h1>
    <p class="text-gray-300 font-light">Your personal path through India's cultural heritage.</p>
</div>

<div class="max-w-5xl mx-auto px-4 py-12 flex flex-col md:flex-row gap-12">
    <!-- Sidebar -->
    <div class="w-full md:w-1/3 space-y-8">
        <div class="bg-white rounded-xl shadow border border-gray-100 p-6 text-center">
            <img src="{{ user.avatar.url|default:'https://ui-avatars.com/api/?name='|add:user.username }}" class="w-24 h-24 rounded-full mx-auto mb-4 border-4 border-gray-50">
            <h3 class="font-bold text-xl text-bharat-navy">{{ user.username }}</h3>
            <span class="text-xs bg-bharat-amber text-bharat-navy px-2 py-1 rounded font-bold uppercase">{{ user.role }}</span>
            
            <div class="mt-6 pt-6 border-t border-gray-100 grid grid-cols-2 gap-4">
                <div>
                    <div class="text-2xl font-bold text-bharat-saffron">{{ user.xp }}</div>
                    <div class="text-xs text-gray-500 uppercase">Cultural XP</div>
                </div>
                <div>
                    <div class="text-2xl font-bold text-bharat-navy">{{ journeys.count }}</div>
                    <div class="text-xs text-gray-500 uppercase">Journeys</div>
                </div>
            </div>
        </div>
        
        <div class="bg-white rounded-xl shadow border border-gray-100 p-6">
            <h4 class="font-bold text-bharat-navy mb-4">+ Create Cultural Journey</h4>
            <form method="POST" action="{% url 'my_journey' %}">
                {% csrf_token %}
                <input type="text" name="title" required placeholder="Journey Title..." class="w-full border border-gray-300 rounded p-2 mb-4">
                <button type="submit" class="w-full bg-bharat-saffron text-white py-2 rounded font-bold hover:bg-orange-600">Create</button>
            </form>
        </div>
    </div>
    
    <!-- Timeline -->
    <div class="w-full md:w-2/3">
        {% if active_journey %}
            <div class="bg-white rounded-xl shadow border border-gray-100 p-8 mb-8">
                <h2 class="text-2xl font-serif font-bold text-bharat-navy mb-2">{{ active_journey.title }}</h2>
                
                <div class="flex justify-between text-sm font-bold text-gray-500 mb-2 mt-6">
                    <span>Progress</span>
                    <span>{{ progress }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-4 mb-8">
                    <div class="bg-green-500 h-4 rounded-full" style="width: {{ progress }}%"></div>
                </div>
                
                <div class="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-300 before:to-transparent">
                    {% for item in items %}
                    <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                        <!-- Icon -->
                        <div class="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-{% if item.completed %}green-500{% else %}slate-200{% endif %} shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow">
                            {% if item.completed %}
                            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            {% endif %}
                        </div>
                        
                        <!-- Card -->
                        <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-4 rounded border border-gray-100 shadow-sm">
                            <h4 class="font-bold text-bharat-navy">{{ item.cultural_entry.title }}</h4>
                            <p class="text-xs text-gray-500 mb-3">{{ item.cultural_entry.category.name }}</p>
                            <div class="flex justify-between items-center">
                                <a href="{% url 'cultural_entry_detail' item.cultural_entry.slug %}" class="text-xs font-bold text-bharat-saffron hover:underline">Read</a>
                                <form action="{% url 'toggle_journey_item' item.id %}" method="POST">
                                    {% csrf_token %}
                                    <button type="submit" class="text-xs font-bold {% if item.completed %}text-gray-400{% else %}text-green-600 hover:bg-green-50 px-2 py-1 rounded border border-green-200{% endif %}">
                                        {% if item.completed %}Completed{% else %}Mark Complete{% endif %}
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <div class="text-center text-gray-500 py-8">
                        No items in this journey yet. Explore India and add entries to your journey!
                    </div>
                    {% endfor %}
                    
                    {% if progress == 100 and items %}
                    <div class="text-center pt-8">
                        <h3 class="text-2xl font-serif font-bold text-green-600 mb-2">Journey Complete! 🎉</h3>
                        <p class="text-gray-600">You've successfully completed this cultural journey.</p>
                    </div>
                    {% endif %}
                </div>
            </div>
        {% else %}
            <div class="text-center py-20 bg-gray-50 rounded-2xl border border-gray-100">
                <h3 class="text-2xl font-serif text-bharat-navy mb-4">No active journeys</h3>
                <p class="text-gray-600 mb-8">Create a journey using the panel on the left to start exploring.</p>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(BASE_DIR, 'templates', 'journeys', 'my_journey.html'), 'w') as f:
    f.write(journey_html)
