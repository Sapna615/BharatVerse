from django.shortcuts import render
from culture.models import CulturalEntry

def home(request):
    featured_entries = CulturalEntry.objects.filter(status='published')[:3]
    regions = ['North India', 'South India', 'East India', 'West India', 'Central India', 'Northeast India']
    return render(request, 'home.html', {
        'featured_entries': featured_entries,
        'regions': regions,
    })

from django.db.models import Q
from culture.models import CulturalEntry, State, Festival, Tradition, FolkArt, Cuisine, CulturalStory, LiteraryWork

def global_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        entries = CulturalEntry.objects.filter(Q(title__icontains=query) | Q(short_description__icontains=query), status='published')
        works = LiteraryWork.objects.filter(
            Q(title__icontains=query) | Q(author_creator__icontains=query) | Q(synopsis__icontains=query) | Q(language__icontains=query) | Q(tradition__icontains=query),
            status='published'
        )
        states = State.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        festivals = Festival.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        stories = CulturalStory.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), moderation_status='approved')
        
        for w in works: results.append({'type': f"Library ({w.get_work_type_display()})", 'title': w.title, 'desc': f"{w.author_creator or 'Classical Tradition'} • {w.language} • {w.brief_intro}", 'url': f'/library/{w.slug}/', 'obj': w})
        for e in entries: results.append({'type': f"Cultural Entry ({e.category.name})", 'title': e.title, 'desc': e.short_description, 'url': f'/explore/culture/{e.slug}/', 'obj': e})
        for s in states: results.append({'type': 'State / Region', 'title': s.name, 'desc': s.description, 'url': f'/explore/states/{s.slug}/', 'obj': s})
        for f in festivals: results.append({'type': 'Festival', 'title': f.name, 'desc': f.description, 'url': f'/explore/calendar/', 'obj': f})
        for st in stories: results.append({'type': 'Oral Story / Heritage Memory', 'title': st.title, 'desc': st.content[:140], 'url': '#', 'obj': st})
        
    return render(request, 'search.html', {'query': query, 'results': results})

