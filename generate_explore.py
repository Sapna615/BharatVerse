import os

BASE_DIR = '/Users/sapnarai/BharatVerse'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

exploration_views = """from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from culture.models import State, CulturalEntry, CulturalConnection, Festival, Tradition, FolkArt, Cuisine
from exploration.models import Favorite
from journeys.models import CulturalJourney, JourneyItem

def explore_india(request):
    region_filter = request.GET.get('region')
    search_query = request.GET.get('q')
    
    states = State.objects.annotate(
        entries_count=Count('entries', distinct=True),
        festivals_count=Count('festivals', distinct=True),
        traditions_count=Count('traditions', distinct=True)
    )
    
    if region_filter:
        states = states.filter(region=region_filter)
    if search_query:
        states = states.filter(name__icontains=search_query)
        
    regions = State.objects.values_list('region', flat=True).distinct()
    
    return render(request, 'exploration/explore_india.html', {
        'states': states,
        'regions': regions,
        'selected_region': region_filter,
        'search_query': search_query
    })

def cultural_map(request):
    states = State.objects.annotate(
        entries_count=Count('entries', distinct=True),
        festivals_count=Count('festivals', distinct=True),
        traditions_count=Count('traditions', distinct=True)
    )
    return render(request, 'exploration/cultural_map.html', {'states': states})

def state_detail(request, slug):
    state = get_object_or_404(State, slug=slug)
    entries = CulturalEntry.objects.filter(state=state, status='published')
    festivals = Festival.objects.filter(state=state)
    traditions = Tradition.objects.filter(state=state)
    arts = FolkArt.objects.filter(state=state)
    cuisines = Cuisine.objects.filter(state=state)
    
    # Calculate fingerprint safely
    fingerprint = {
        'Dance': entries.filter(category__name__iexact='Dance').count(),
        'Music': entries.filter(category__name__iexact='Music').count(),
        'Craft': entries.filter(category__name__iexact='Craft').count(),
        'Cuisine': cuisines.count(),
        'Festivals': festivals.count(),
        'Stories': entries.filter(category__name__iexact='Story').count(),
    }
    # find max for percentage calculation in template
    max_val = max(fingerprint.values()) if fingerprint.values() else 1
    if max_val == 0: max_val = 1
    
    for k in fingerprint:
        fingerprint[k] = int((fingerprint[k] / max_val) * 100)
    
    return render(request, 'culture/state_detail.html', {
        'state': state,
        'entries': entries,
        'festivals': festivals,
        'traditions': traditions,
        'arts': arts,
        'cuisines': cuisines,
        'fingerprint': fingerprint
    })

def cultural_entry_detail(request, slug):
    entry = get_object_or_404(CulturalEntry, slug=slug, status='published')
    connections = CulturalConnection.objects.filter(source_entry=entry) | CulturalConnection.objects.filter(target_entry=entry)
    
    is_favorite = False
    user_journeys = []
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, cultural_entry=entry).exists()
        user_journeys = CulturalJourney.objects.filter(user=request.user)
        
    return render(request, 'culture/cultural_entry.html', {
        'entry': entry,
        'connections': connections[:3],
        'is_favorite': is_favorite,
        'user_journeys': user_journeys
    })

def cultural_connections(request, slug):
    entry = get_object_or_404(CulturalEntry, slug=slug, status='published')
    source_conns = CulturalConnection.objects.filter(source_entry=entry)
    target_conns = CulturalConnection.objects.filter(target_entry=entry)
    
    return render(request, 'culture/connections.html', {
        'entry': entry,
        'source_conns': source_conns,
        'target_conns': target_conns,
    })

@login_required
def toggle_favorite(request, slug):
    entry = get_object_or_404(CulturalEntry, slug=slug)
    fav, created = Favorite.objects.get_or_create(user=request.user, cultural_entry=entry)
    if not created:
        fav.delete()
        messages.info(request, 'Removed from Favorites.')
    else:
        messages.success(request, 'Saved to My Favorites.')
    return redirect('cultural_entry_detail', slug=slug)

@login_required
def add_to_journey(request, slug):
    if request.method == 'POST':
        entry = get_object_or_404(CulturalEntry, slug=slug)
        journey_id = request.POST.get('journey_id')
        if journey_id:
            journey = get_object_or_404(CulturalJourney, id=journey_id, user=request.user)
            item, created = JourneyItem.objects.get_or_create(journey=journey, cultural_entry=entry)
            if created:
                messages.success(request, f'Added to {journey.title}.')
            else:
                messages.info(request, f'Already in {journey.title}.')
        else:
            messages.error(request, 'Please select a valid journey.')
    return redirect('cultural_entry_detail', slug=slug)
"""

exploration_urls = """from django.urls import path
from .views import (explore_india, cultural_map, state_detail, 
                    cultural_entry_detail, cultural_connections,
                    toggle_favorite, add_to_journey)

urlpatterns = [
    path('', explore_india, name='explore_india'),
    path('map/', cultural_map, name='cultural_map'),
    path('states/<slug:slug>/', state_detail, name='state_detail'),
    path('culture/<slug:slug>/', cultural_entry_detail, name='cultural_entry_detail'),
    path('connections/<slug:slug>/', cultural_connections, name='cultural_connections'),
    path('culture/<slug:slug>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('culture/<slug:slug>/add-to-journey/', add_to_journey, name='add_to_journey'),
]
"""

explore_india_html = """{% extends 'base.html' %}
{% block title %}Explore India - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl md:text-5xl font-serif font-bold text-white mb-4">Explore India</h1>
        <p class="text-xl text-gray-300 font-light max-w-2xl mx-auto">Every region tells a different story. Explore the traditions that connect us.</p>
    </div>
</div>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Filters -->
    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8 flex flex-col md:flex-row gap-4 items-center justify-between">
        <form class="flex-grow flex gap-4 w-full md:w-auto" method="GET" action="{% url 'explore_india' %}">
            <input type="text" name="q" placeholder="Search states..." value="{{ search_query|default:'' }}" class="flex-grow border border-gray-300 rounded-md px-4 py-2 focus:ring-bharat-saffron focus:border-bharat-saffron">
            <select name="region" class="border border-gray-300 rounded-md px-4 py-2 focus:ring-bharat-saffron focus:border-bharat-saffron">
                <option value="">All Regions</option>
                {% for r in regions %}
                <option value="{{ r }}" {% if selected_region == r %}selected{% endif %}>{{ r }}</option>
                {% endfor %}
            </select>
            <button type="submit" class="bg-bharat-saffron text-white px-6 py-2 rounded-md hover:bg-orange-600 font-medium transition">Filter</button>
            <a href="{% url 'cultural_map' %}" class="bg-bharat-amber text-bharat-navy px-6 py-2 rounded-md hover:bg-yellow-500 font-medium transition ml-auto">Interactive Map View &rarr;</a>
        </form>
    </div>

    <!-- State Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {% for state in states %}
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition group">
            <div class="p-6">
                <span class="text-xs font-bold text-bharat-saffron uppercase tracking-wider mb-2 block">{{ state.region }}</span>
                <h2 class="text-2xl font-serif font-bold text-bharat-navy mb-2">{{ state.name }}</h2>
                <p class="text-gray-600 text-sm mb-6 line-clamp-2">{{ state.description }}</p>
                
                <div class="flex gap-4 mb-6 border-t border-gray-100 pt-4">
                    <div class="text-center flex-1">
                        <div class="text-xl font-bold text-bharat-navy">{{ state.entries_count }}</div>
                        <div class="text-xs text-gray-500">Entries</div>
                    </div>
                    <div class="text-center flex-1 border-l border-r border-gray-100">
                        <div class="text-xl font-bold text-bharat-navy">{{ state.festivals_count }}</div>
                        <div class="text-xs text-gray-500">Festivals</div>
                    </div>
                    <div class="text-center flex-1">
                        <div class="text-xl font-bold text-bharat-navy">{{ state.traditions_count }}</div>
                        <div class="text-xs text-gray-500">Traditions</div>
                    </div>
                </div>
                
                <a href="{% url 'state_detail' state.slug %}" class="block w-full text-center bg-gray-50 text-bharat-navy font-semibold py-3 rounded-lg group-hover:bg-bharat-saffron group-hover:text-white transition">Explore {{ state.name }}</a>
            </div>
        </div>
        {% empty %}
        <div class="col-span-3 text-center py-12">
            <p class="text-gray-500 text-lg">No states found matching your criteria.</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""

cultural_map_html = """{% extends 'base.html' %}
{% block title %}Cultural Map - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">Cultural Map of India</h1>
    <p class="text-gray-300 font-light">Choose a region. Discover its culture.</p>
</div>

<div class="max-w-7xl mx-auto px-4 py-8 flex flex-col lg:flex-row gap-8">
    <!-- Fake Map Region Explorer due to strict constraints on geospatial boundaries -->
    <div class="lg:w-2/3 bg-white rounded-xl shadow p-6 border border-gray-100">
        <h3 class="text-xl font-bold text-bharat-navy mb-4 border-b pb-2">Regional Explorer</h3>
        <p class="text-sm text-gray-500 mb-6">Select a state below to view its cultural snapshot.</p>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            {% for state in states %}
            <div class="border border-gray-200 rounded p-4 text-center cursor-pointer hover:border-bharat-saffron hover:bg-orange-50 transition" onclick="showStateInfo('{{ state.name }}', '{{ state.region }}', {{ state.entries_count }}, {{ state.festivals_count }}, '{{ state.slug }}')">
                <span class="font-bold text-bharat-navy">{{ state.name }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <!-- Info Panel -->
    <div class="lg:w-1/3">
        <div id="info-panel" class="bg-bharat-cream rounded-xl shadow-lg p-8 border border-gray-200 sticky top-24 hidden">
            <span id="p-region" class="text-sm font-bold text-bharat-saffron uppercase tracking-wider mb-2 block">Region</span>
            <h2 id="p-name" class="text-3xl font-serif font-bold text-bharat-navy mb-4">State Name</h2>
            
            <div class="space-y-4 mb-8">
                <div class="flex justify-between items-center border-b border-gray-200 pb-2">
                    <span class="text-gray-600">Cultural Entries</span>
                    <span id="p-entries" class="font-bold text-bharat-navy">0</span>
                </div>
                <div class="flex justify-between items-center border-b border-gray-200 pb-2">
                    <span class="text-gray-600">Festivals</span>
                    <span id="p-festivals" class="font-bold text-bharat-navy">0</span>
                </div>
            </div>
            
            <a id="p-link" href="#" class="block w-full text-center bg-bharat-amber text-bharat-navy font-bold py-3 rounded-lg hover:bg-yellow-500 transition shadow">Explore State</a>
        </div>
        <div id="info-empty" class="bg-gray-50 rounded-xl border border-gray-200 p-8 text-center text-gray-500 h-64 flex items-center justify-center">
            Select a state from the explorer to view details.
        </div>
    </div>
</div>

<script>
    function showStateInfo(name, region, entries, festivals, slug) {
        document.getElementById('info-empty').classList.add('hidden');
        document.getElementById('info-panel').classList.remove('hidden');
        
        document.getElementById('p-name').innerText = name;
        document.getElementById('p-region').innerText = region;
        document.getElementById('p-entries').innerText = entries;
        document.getElementById('p-festivals').innerText = festivals;
        document.getElementById('p-link').href = '/explore/states/' + slug + '/';
    }
</script>
{% endblock %}
"""

state_detail_html = """{% extends 'base.html' %}
{% block title %}Discover {{ state.name }} - BharatVerse{% endblock %}
{% block content %}
<!-- Hero Section -->
<div class="bg-bharat-navy py-20 text-center relative overflow-hidden">
    <div class="relative z-10 max-w-4xl mx-auto px-4">
        <span class="text-bharat-saffron font-bold tracking-widest uppercase text-sm mb-4 block">{{ state.region }}</span>
        <h1 class="text-5xl md:text-6xl font-serif font-bold text-white mb-6">Discover {{ state.name }}</h1>
        <p class="text-xl text-gray-300 font-light mb-8">{{ state.description }}</p>
        <div class="flex justify-center gap-4">
            <a href="#explore" class="bg-bharat-saffron hover:bg-orange-600 text-white font-bold py-3 px-8 rounded-full shadow transition">Explore Its Culture</a>
        </div>
    </div>
</div>

<!-- Fingerprint Section -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 md:p-12">
        <div class="text-center mb-10">
            <h2 class="text-3xl font-serif font-bold text-bharat-navy mb-4">Cultural Fingerprint</h2>
            <p class="text-gray-500">A visual snapshot of what makes this region culturally distinctive in our database.</p>
        </div>
        
        <div class="max-w-3xl mx-auto space-y-6">
            {% for category, percentage in fingerprint.items %}
            <div>
                <div class="flex justify-between text-sm font-bold text-bharat-navy mb-1">
                    <span>{{ category }}</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-3">
                    <div class="bg-bharat-saffron h-3 rounded-full" style="width: {{ percentage }}%"></div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<!-- Content Grid -->
<div id="explore" class="bg-gray-50 py-16 border-t border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {% if entries %}
        <div class="mb-16">
            <h3 class="text-2xl font-serif font-bold text-bharat-navy mb-8 border-b-2 border-bharat-saffron inline-block pb-2">Cultural Stories</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {% for entry in entries %}
                <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition p-6 border border-gray-100">
                    <span class="text-xs font-bold text-gray-500 uppercase">{{ entry.category.name }}</span>
                    <h4 class="text-xl font-bold text-bharat-navy mt-1 mb-2">{{ entry.title }}</h4>
                    <p class="text-sm text-gray-600 line-clamp-3 mb-4">{{ entry.short_description }}</p>
                    <a href="{% url 'cultural_entry_detail' entry.slug %}" class="text-bharat-amber font-semibold hover:text-yellow-600">Read More &rarr;</a>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if festivals %}
        <div class="mb-16">
            <h3 class="text-2xl font-serif font-bold text-bharat-navy mb-8 border-b-2 border-bharat-saffron inline-block pb-2">Festivals</h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                {% for festival in festivals %}
                <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
                    <span class="text-xs font-bold text-bharat-saffron uppercase block mb-1">{{ festival.month }}</span>
                    <h4 class="text-lg font-bold text-bharat-navy mb-2">{{ festival.name }}</h4>
                    <p class="text-sm text-gray-600">{{ festival.description }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if not entries and not festivals and not traditions %}
        <div class="text-center py-20">
            <h3 class="text-2xl font-serif text-gray-400 mb-2">We're still adding stories from this region.</h3>
            <p class="text-gray-500">Check back later or become a contributor!</p>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
"""

cultural_entry_html = """{% extends 'base.html' %}
{% block title %}{{ entry.title }} - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-16">
    <div class="max-w-4xl mx-auto px-4 text-center">
        <span class="text-bharat-amber font-bold tracking-widest uppercase text-sm mb-4 block">{{ entry.state.name }} &middot; {{ entry.category.name }}</span>
        <h1 class="text-5xl font-serif font-bold text-white mb-6">{{ entry.title }}</h1>
        <p class="text-xl text-gray-300 font-light mb-8 max-w-3xl mx-auto">{{ entry.short_description }}</p>
        
        <div class="flex flex-wrap justify-center gap-4">
            <form action="{% url 'toggle_favorite' entry.slug %}" method="POST" class="inline">
                {% csrf_token %}
                <button type="submit" class="bg-white text-bharat-navy font-bold py-3 px-6 rounded-full shadow hover:bg-gray-100 transition flex items-center gap-2">
                    {% if is_favorite %}❤️ Saved{% else %}🤍 Save{% endif %}
                </button>
            </form>
            <button onclick="document.getElementById('journey-modal').classList.remove('hidden')" class="bg-bharat-saffron text-white font-bold py-3 px-6 rounded-full shadow hover:bg-orange-600 transition flex items-center gap-2">
                ➕ Add to Journey
            </button>
            <a href="{% url 'cultural_connections' entry.slug %}" class="bg-transparent border-2 border-bharat-amber text-bharat-amber hover:bg-bharat-amber hover:text-bharat-navy font-bold py-3 px-6 rounded-full transition flex items-center gap-2">
                🎯 Explore Connections
            </a>
            <button class="bg-gray-800 text-gray-300 border border-gray-600 font-bold py-3 px-6 rounded-full hover:bg-gray-700 transition flex items-center gap-2">
                🤖 Ask AI (Demo)
            </button>
        </div>
    </div>
</div>

<div class="max-w-4xl mx-auto px-4 py-16">
    <div class="prose prose-lg mx-auto">
        <h2 class="text-3xl font-serif font-bold text-bharat-navy mb-6">The Story</h2>
        <p class="text-gray-700 leading-relaxed mb-10">{{ entry.detailed_story|linebreaks }}</p>
        
        <h2 class="text-3xl font-serif font-bold text-bharat-navy mb-6">Why It Matters</h2>
        <p class="text-gray-700 leading-relaxed mb-10">{{ entry.cultural_significance|linebreaks }}</p>
        
        <h2 class="text-3xl font-serif font-bold text-bharat-navy mb-6">How It Is Practiced</h2>
        <p class="text-gray-700 leading-relaxed mb-10">{{ entry.practice_description|linebreaks }}</p>
    </div>
    
    {% if connections %}
    <div class="mt-16 bg-gray-50 rounded-2xl p-8 border border-gray-200">
        <h3 class="text-2xl font-serif font-bold text-bharat-navy mb-6">How It Connects</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {% for conn in connections %}
                <div class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm text-center">
                    <span class="text-xs text-gray-500 uppercase">{{ conn.relationship_type }}</span>
                    <h4 class="font-bold text-bharat-navy mt-1">{% if conn.source_entry == entry %}{{ conn.target_entry.title }}{% else %}{{ conn.source_entry.title }}{% endif %}</h4>
                </div>
            {% endfor %}
        </div>
        <div class="text-center">
            <a href="{% url 'cultural_connections' entry.slug %}" class="text-bharat-saffron font-bold hover:underline">Explore All Connections &rarr;</a>
        </div>
    </div>
    {% endif %}
</div>

<!-- Journey Modal -->
<div id="journey-modal" class="fixed inset-0 bg-gray-900 bg-opacity-50 hidden flex justify-center items-center z-50">
    <div class="bg-white rounded-xl shadow-xl p-8 max-w-md w-full m-4">
        <h3 class="text-2xl font-serif font-bold text-bharat-navy mb-4">Add to Journey</h3>
        {% if not user.is_authenticated %}
            <p class="text-gray-600 mb-6">Please log in to add this to your cultural journey.</p>
            <div class="flex justify-end gap-4">
                <button onclick="document.getElementById('journey-modal').classList.add('hidden')" class="text-gray-500 hover:text-gray-700">Cancel</button>
                <a href="{% url 'login' %}" class="bg-bharat-saffron text-white px-4 py-2 rounded-md font-bold shadow">Log in</a>
            </div>
        {% else %}
            {% if user_journeys %}
            <form action="{% url 'add_to_journey' entry.slug %}" method="POST">
                {% csrf_token %}
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Journey</label>
                    <select name="journey_id" class="w-full border border-gray-300 rounded-md p-2 focus:ring-bharat-saffron focus:border-bharat-saffron">
                        {% for j in user_journeys %}
                        <option value="{{ j.id }}">{{ j.title }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="flex justify-end gap-4">
                    <button type="button" onclick="document.getElementById('journey-modal').classList.add('hidden')" class="text-gray-500 hover:text-gray-700">Cancel</button>
                    <button type="submit" class="bg-bharat-saffron text-white px-4 py-2 rounded-md font-bold shadow hover:bg-orange-600">Add</button>
                </div>
            </form>
            {% else %}
                <p class="text-gray-600 mb-6">You don't have any active journeys. Please create one in your dashboard first.</p>
                <div class="flex justify-end">
                    <button type="button" onclick="document.getElementById('journey-modal').classList.add('hidden')" class="text-gray-500 hover:text-gray-700">Close</button>
                </div>
            {% endif %}
        {% endif %}
    </div>
</div>
{% endblock %}
"""

connections_html = """{% extends 'base.html' %}
{% block title %}Connections: {{ entry.title }} - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">How Culture Connects</h1>
    <p class="text-gray-300 font-light">Culture does not exist in isolation. Explore the relationships.</p>
</div>

<div class="max-w-7xl mx-auto px-4 py-16">
    <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 text-center max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold text-bharat-navy mb-8">Central Entity: <span class="text-bharat-saffron">{{ entry.title }}</span></h2>
        
        <div class="flex flex-col md:flex-row justify-center items-center gap-8 md:gap-16">
            
            <!-- Source Connections -->
            <div class="space-y-4">
                <h3 class="text-sm font-bold text-gray-500 uppercase tracking-widest mb-4">Relates To</h3>
                {% for conn in source_conns %}
                <a href="{% url 'cultural_entry_detail' conn.target_entry.slug %}" class="block bg-gray-50 hover:bg-orange-50 border border-gray-200 hover:border-bharat-saffron rounded-xl p-4 transition text-left group">
                    <div class="text-xs text-bharat-saffron font-bold mb-1">{{ conn.relationship_type }}</div>
                    <div class="font-bold text-bharat-navy group-hover:text-orange-600">{{ conn.target_entry.title }}</div>
                    <div class="text-xs text-gray-500 mt-1 line-clamp-2">{{ conn.description }}</div>
                </a>
                {% empty %}
                <div class="text-gray-400 italic text-sm">No forward connections mapped yet.</div>
                {% endfor %}
            </div>
            
            <!-- The Entry Node -->
            <div class="w-32 h-32 rounded-full bg-gradient-to-br from-bharat-saffron to-bharat-amber flex items-center justify-center text-white font-bold shadow-xl border-4 border-white z-10 shrink-0 transform hover:scale-105 transition cursor-pointer">
                <div class="text-center">
                    <div class="text-lg leading-tight">{{ entry.title }}</div>
                </div>
            </div>
            
            <!-- Target Connections -->
            <div class="space-y-4">
                <h3 class="text-sm font-bold text-gray-500 uppercase tracking-widest mb-4">Related From</h3>
                {% for conn in target_conns %}
                <a href="{% url 'cultural_entry_detail' conn.source_entry.slug %}" class="block bg-gray-50 hover:bg-orange-50 border border-gray-200 hover:border-bharat-saffron rounded-xl p-4 transition text-left group">
                    <div class="text-xs text-bharat-saffron font-bold mb-1">{{ conn.relationship_type }}</div>
                    <div class="font-bold text-bharat-navy group-hover:text-orange-600">{{ conn.source_entry.title }}</div>
                    <div class="text-xs text-gray-500 mt-1 line-clamp-2">{{ conn.description }}</div>
                </a>
                {% empty %}
                <div class="text-gray-400 italic text-sm">No reverse connections mapped yet.</div>
                {% endfor %}
            </div>
            
        </div>
        
        <div class="mt-12 pt-8 border-t border-gray-100">
            <a href="{% url 'cultural_entry_detail' entry.slug %}" class="text-bharat-navy font-bold hover:text-bharat-saffron transition">&larr; Back to {{ entry.title }}</a>
        </div>
    </div>
</div>
{% endblock %}
"""

bharatverse_urls_update = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('explore/', include('exploration.urls')),
    path('api/', include('culture.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""

files = {
    'exploration/views.py': exploration_views,
    'exploration/urls.py': exploration_urls,
    'templates/exploration/explore_india.html': explore_india_html,
    'templates/exploration/cultural_map.html': cultural_map_html,
    'templates/culture/state_detail.html': state_detail_html,
    'templates/culture/cultural_entry.html': cultural_entry_html,
    'templates/culture/connections.html': connections_html,
    'bharatverse/urls.py': bharatverse_urls_update,
}

for path, content in files.items():
    with open(os.path.join(BASE_DIR, path), 'w') as f:
        f.write(content)
    print(f"Generated {path}")
