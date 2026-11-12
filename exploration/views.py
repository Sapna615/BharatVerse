from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
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

import json

def cultural_map(request):
    states = State.objects.annotate(
        entries_count=Count('entries', distinct=True),
        festivals_count=Count('festivals', distinct=True),
        cuisines_count=Count('cuisines', distinct=True)
    ).order_by('name')
    
    states_dict = {}
    for s in states:
        entries = CulturalEntry.objects.filter(state=s, status='published')
        festivals = Festival.objects.filter(state=s)
        cuisines = Cuisine.objects.filter(state=s)
        
        dance_count = entries.filter(category__name__icontains='Dance').count()
        music_count = entries.filter(category__name__icontains='Music').count()
        craft_count = entries.filter(category__name__icontains='Craft').count()
        story_count = entries.filter(category__name__icontains='Story').count()
        fest_count = festivals.count()
        cuisine_count = cuisines.count()
        
        categories = []
        if dance_count > 0:
            categories.append({'name': 'Dance & Performing Arts', 'short': 'Dance', 'count': dance_count, 'icon': 'fas fa-theater-masks', 'color': 'rose'})
        if music_count > 0:
            categories.append({'name': 'Music & Instruments', 'short': 'Music', 'count': music_count, 'icon': 'fas fa-music', 'color': 'indigo'})
        if craft_count > 0:
            categories.append({'name': 'Crafts & Textiles', 'short': 'Crafts', 'count': craft_count, 'icon': 'fas fa-palette', 'color': 'emerald'})
        if cuisine_count > 0:
            categories.append({'name': 'Food & Cuisine', 'short': 'Cuisine', 'count': cuisine_count, 'icon': 'fas fa-utensils', 'color': 'amber'})
        if fest_count > 0:
            categories.append({'name': 'Festivals & Living Traditions', 'short': 'Festivals', 'count': fest_count, 'icon': 'fas fa-fire-alt', 'color': 'orange'})
        if story_count > 0:
            categories.append({'name': 'Stories & Folklore', 'short': 'Stories', 'count': story_count, 'icon': 'fas fa-book-open', 'color': 'purple'})
            
        featured = []
        for e in entries[:4]:
            featured.append({
                'title': e.title,
                'category': e.category.name,
                'slug': e.slug,
                'desc': (e.short_description[:110] + '...') if len(e.short_description) > 110 else e.short_description,
                'url': f'/explore/culture/{e.slug}/'
            })
            
        states_dict[s.slug] = {
            'name': s.name,
            'slug': s.slug,
            'region': s.region,
            'description': s.description or f"Discover the rich cultural heritage and timeless traditions of {s.name}.",
            'summary': s.cultural_summary or f"Explore the artistic, musical, culinary, and festive landscape of {s.name}.",
            'counts': {
                'entries': entries.count(),
                'festivals': fest_count,
                'cuisines': cuisine_count,
                'total': entries.count() + fest_count + cuisine_count
            },
            'categories': categories,
            'featured': featured,
            'url': f'/explore/states/{s.slug}/',
            'connections_url': f'/explore/connections/{featured[0]["slug"]}/' if featured else f'/explore/states/{s.slug}/'
        }
        
    regions = sorted(list(set(s.region for s in states if s.region)))
    
    return render(request, 'exploration/cultural_map.html', {
        'states': states,
        'states_dict_json': json.dumps(states_dict),
        'regions': regions,
    })

def state_detail(request, slug):
    state = get_object_or_404(State, slug=slug)
    entries = CulturalEntry.objects.filter(state=state, status='published')
    dance_entries = entries.filter(category__name__icontains='Dance')
    music_entries = entries.filter(category__name__icontains='Music')
    craft_entries = entries.filter(category__name__icontains='Craft')
    story_entries = entries.filter(category__name__icontains='Story')
    
    festivals = Festival.objects.filter(state=state)
    traditions = Tradition.objects.filter(state=state)
    arts = FolkArt.objects.filter(state=state)
    cuisines = Cuisine.objects.filter(state=state)
    community_stories = state.culturalstory_set.filter(moderation_status='approved')
    
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
        'dance_entries': dance_entries,
        'music_entries': music_entries,
        'craft_entries': craft_entries,
        'story_entries': story_entries,
        'festivals': festivals,
        'traditions': traditions,
        'arts': arts,
        'cuisines': cuisines,
        'community_stories': community_stories,
        'fingerprint': fingerprint
    })

def get_experience_metadata(entry):
    cat_name = entry.category.name.lower()
    title_lower = entry.title.lower()
    
    # Specific highlight for Blue Pottery
    if 'blue pottery' in title_lower:
        return {
            'sensory_signatures': [
                {'icon': 'fas fa-palette', 'title': 'Color Palette', 'detail': 'Vivid Cobalt Blue & Copper Turquoise on milky white quartz base'},
                {'icon': 'fas fa-gem', 'title': 'Mineral Sheen', 'detail': 'Vitreous, translucent glass glaze fired at 850°C'},
                {'icon': 'fas fa-hand-holding-heart', 'title': 'Tactile Feel', 'detail': 'Cool, lightweight semi-vitrified texture with zero clay porosity'},
                {'icon': 'fas fa-feather', 'title': 'Brushwork', 'detail': 'Freehand squirrel-hair miniature brush detailing without stencils'}
            ],
            'workshop_stages': [
                {'step': '01', 'title': 'Mineral Alchemy', 'desc': 'Kneading crushed quartz stone, recycled glass (cullet), Multani mitti, and natural gum into a pliable dough.'},
                {'step': '02', 'title': 'Open-Mould Shaping', 'desc': 'Dough is rolled into flat discs, pressed into plaster-of-Paris moulds, and filled with wood ash to cure in the sun.'},
                {'step': '03', 'title': 'Freehand Painting', 'desc': 'Master artisans hand-paint traditional motifs using cobalt oxide (blue) and copper oxide (turquoise).'},
                {'step': '04', 'title': 'Single-Fire Vitrification', 'desc': 'Coated in non-toxic glaze and baked for 72 hours in an 850°C kiln, cooling slowly to lock in gem-like brilliance.'}
            ],
            'where_to_experience': [
                {'place': 'Kot Jewar Artisan Cluster', 'city': 'Jaipur Rural', 'desc': 'Visit generational potter families and witness open-flame kilns in action.'},
                {'place': 'Kripal Kumbh Studio', 'city': 'Bani Park, Jaipur', 'desc': 'The legendary studio of revivalist Padma Shri Kripal Singh Shekhawat.'},
                {'place': 'Bapu & Johari Bazaars', 'city': 'Walled City, Jaipur', 'desc': 'Curated heritage shops offering certified GI-tagged handcrafted blue pottery.'}
            ],
            'curator_facts': [
                {'title': '100% Clay-Free Mystery', 'fact': 'Jaipur Blue Pottery is the only major pottery tradition on Earth made entirely without clay (mitti), relying instead on quartz.'},
                {'title': 'The Royal Kite Duel Legend', 'fact': 'Maharaja Sawai Ram Singh II discovered the potters after their glass-coated kite strings repeatedly severed the royal kites!'},
                {'title': 'Single-Firing Mastery', 'fact': 'Unlike conventional double-fired pottery, authentic blue pottery is vitrified in a single 72-hour kiln firing.'}
            ],
            'quiz': {
                'question': 'Which primary mineral compound gives Jaipur Blue Pottery its signature royal blue color?',
                'options': ['Red Ochre Clay', 'Cobalt Oxide', 'Ground Turmeric Root', 'Lapis Lazuli Paste'],
                'correct_index': 1,
                'explanation': 'Cobalt oxide is the mineral pigment that vitrifies during the 850°C kiln firing into permanent deep royal blue!'
            }
        }
    
    # Generic category fallbacks
    if 'dance' in cat_name:
        return {
            'sensory_signatures': [
                {'icon': 'fas fa-drum', 'title': 'Rhythmic Taal', 'detail': 'Complex syncopated footwork synchronized with live percussion'},
                {'icon': 'fas fa-theater-masks', 'title': 'Bhavas & Abhinaya', 'detail': 'Expressive eye movements, brow tilts, and micro-expressions'},
                {'icon': 'fas fa-bell', 'title': 'Acoustic Ghungroos', 'detail': 'Polished brass ankle bells chiming in musical subdivision'},
                {'icon': 'fas fa-tshirt', 'title': 'Costume Geometry', 'detail': 'Handloom silk pleats and traditional gilded crowns/headpieces'}
            ],
            'workshop_stages': [
                {'step': '01', 'title': 'Bhumi Pranam', 'desc': 'Reverence paid to Mother Earth, the guru, and the divine stage before the first step.'},
                {'step': '02', 'title': 'Adavus & Footwork', 'desc': 'Mastery of fundamental postures, leg extensions, and rhythmic syllables (Jathis).'},
                {'step': '03', 'title': 'Hasta Mudras', 'desc': 'Learning the 24+ codified hand gestures capable of telling entire epic sagas.'},
                {'step': '04', 'title': 'Performance & Sabha', 'desc': 'Ascending the sacred performance stage with live orchestral accompaniment.'}
            ],
            'where_to_experience': [
                {'place': 'Annual Heritage Festivals', 'city': f'{entry.state.name}', 'desc': 'Witness live master dancers perform in temple courtyards and open-air amphitheatres.'},
                {'place': 'State Performing Academies', 'city': f'{entry.state.name}', 'desc': 'Observe students learning generational techniques under guru-shishya parampara.'},
                {'place': 'Community Celebrations', 'city': f'{entry.state.name}', 'desc': 'Experience spontaneous folk dances during regional harvest and seasonal festivals.'}
            ],
            'curator_facts': [
                {'title': 'Ancient Living Heritage', 'fact': f'{entry.title} has survived across generations through sacred oral memory and guru-shishya lineages.'},
                {'title': 'Language of Mudras', 'fact': 'Dancers can communicate hundreds of precise mythological narratives without uttering a single spoken word.'},
                {'title': 'Cosmic Rhythm', 'fact': 'Traditional Indian dance philosophy views bodily movement as an alignment with cosmic geometry.'}
            ],
            'quiz': {
                'question': f'What is the traditional opening gesture of reverence before performing {entry.title}?',
                'options': ['Bhumi Pranam (Reverence to Earth)', 'Tandava Leap', 'Fast Pirouette', 'Cymbal Strike'],
                'correct_index': 0,
                'explanation': 'Dancers always perform Bhumi Pranam to seek forgiveness and blessing from Mother Earth before stamping their feet!'
            }
        }
    elif 'music' in cat_name:
        return {
            'sensory_signatures': [
                {'icon': 'fas fa-music', 'title': 'Tonal Resonance', 'detail': 'Acoustic vibrations crafted from seasoned jackwood, rosewood, or dried gourds'},
                {'icon': 'fas fa-wave-square', 'title': 'Microtones & Gamakas', 'detail': 'Delicate pitch glides and embellishments between notes (swaras)'},
                {'icon': 'fas fa-heartbeat', 'title': 'Tala Cycles', 'detail': 'Cyclic rhythmic frameworks ranging from 6 to 16 beats per cycle'},
                {'icon': 'fas fa-sun', 'title': 'Raga Time Theory', 'detail': 'Specific melodies performed at dawn, dusk, or midnight to match nature'}
            ],
            'workshop_stages': [
                {'step': '01', 'title': 'Riyaaz / Tuning', 'desc': 'Dawn acoustic tuning and scale practice aligning the artist with the drone.'},
                {'step': '02', 'title': 'Alap / Unfolding', 'desc': 'Slow, meditative exploration of notes without rhythm to establish the raga mood.'},
                {'step': '03', 'title': 'Bandish & Composition', 'desc': 'Introducing the poetic composition accompanied by steady percussion pulses.'},
                {'step': '04', 'title': 'Jhala / Crescendo', 'desc': 'High-tempo rhythmic dialogue culminating in breathtaking syncopated tihai finishes.'}
            ],
            'where_to_experience': [
                {'place': 'Classical Heritage Sabhas', 'city': f'{entry.state.name}', 'desc': 'Intimate baithaks and concert halls known for supreme acoustic purity.'},
                {'place': 'Temple Dawn Ceremonies', 'city': f'{entry.state.name}', 'desc': 'Sacred morning Mangala Vadya recitals accompanying deity awakenings.'},
                {'place': 'Master Luthier Workshops', 'city': f'{entry.state.name}', 'desc': 'Artisan quarters where instruments are hand-chiseled and tuned by ear.'}
            ],
            'curator_facts': [
                {'title': 'Natural Acoustic Alchemy', 'fact': 'Instruments utilize natural resonance chambers like dried bottle gourds, aged jackwood, and animal parchment.'},
                {'title': 'Spiritual Intention', 'fact': 'In Indian music philosophy, sound (Naada Brahma) is considered a direct path to self-realization.'},
                {'title': 'Improvisation Supremacy', 'fact': 'Up to 80% of a classical Indian performance is spontaneously improvised within the raga framework.'}
            ],
            'quiz': {
                'question': f'Which element sets the foundational pitch drone for {entry.title}?',
                'options': ['Tambura / Drone string', 'Brass Bell', 'Snare Drum', 'Synthetic Synthesizer'],
                'correct_index': 0,
                'explanation': 'The continuous acoustic drone (tanpura/shruti) establishes the tonic root note (Sa) that anchors the entire performance!'
            }
        }
    elif 'craft' in cat_name:
        return {
            'sensory_signatures': [
                {'icon': 'fas fa-palette', 'title': 'Natural Dye Palette', 'detail': 'Pigments derived from madder root, indigo leaves, turmeric, and minerals'},
                {'icon': 'fas fa-feather', 'title': 'Handmade Texture', 'detail': 'Irregular slubs and unique artisan impressions that distinguish authentic work'},
                {'icon': 'fas fa-shapes', 'title': 'Symbolic Motifs', 'detail': 'Flora, fauna, and geometric talismans conveying blessings and protection'},
                {'icon': 'fas fa-leaf', 'title': 'Zero-Waste Philosophy', 'detail': 'Eco-friendly indigenous materials sustainably harvested from the local bioregion'}
            ],
            'workshop_stages': [
                {'step': '01', 'title': 'Raw Fibre / Mineral Prep', 'desc': 'Sorting, spinning, or grinding raw organic materials using time-tested tools.'},
                {'step': '02', 'title': 'Structural Shaping', 'desc': 'Setting the warp and weft on wooden looms, or sculpting moulds by hand.'},
                {'step': '03', 'title': 'Hand Detailing', 'desc': 'Delicate embroidery, block-stamping, metal-chasing, or freehand painting.'},
                {'step': '04', 'title': 'Finishing & Vitrification', 'desc': 'Sun-bleaching, washing in river currents, or open-flame kiln baking.'}
            ],
            'where_to_experience': [
                {'place': 'Rural Artisan Clusters', 'city': f'{entry.state.name}', 'desc': 'Heritage villages where entire streets function as collaborative family workshops.'},
                {'place': 'State Handicraft Emporiums', 'city': f'{entry.state.name}', 'desc': 'Certified government craft centers ensuring fair remuneration for weavers and artisans.'},
                {'place': 'National Crafts Melas', 'city': 'Pan-India', 'desc': 'Direct interactions with national award-winning master craftsmen and women.'}
            ],
            'curator_facts': [
                {'title': 'Generational Memory', 'fact': 'Motifs and techniques are committed to memory through mnemonic songs rather than blueprints.'},
                {'title': 'Geographical Indication (GI)', 'fact': 'Recognized by GI protection to defend against industrial machine counterfeits.'},
                {'title': 'Sustainable Luxury', 'fact': 'Handcrafted with minimal carbon footprints using natural biological and mineral elements.'}
            ],
            'quiz': {
                'question': f'What is the defining hallmark of authentic handmade {entry.title}?',
                'options': ['Handcrafted organic variations', 'Laser-cut identical plastic edges', 'Synthetic polyester coating', 'Industrial machine stamping'],
                'correct_index': 0,
                'explanation': 'Subtle handcrafted variations are the fingerprint of human artisanal mastery and prove genuine pedigree!'
            }
        }
    else:
        return {
            'sensory_signatures': [
                {'icon': 'fas fa-book-reader', 'title': 'Oral Cadence', 'detail': 'Rhythmic poetic verse, dramatic pauses, and evocative vocal dynamics'},
                {'icon': 'fas fa-crown', 'title': 'Heroic Archetypes', 'detail': 'Kings, wandering ascetics, celestial lovers, and righteous rebels'},
                {'icon': 'fas fa-fire', 'title': 'Dramatic Tension', 'detail': 'Moral dilemmas and tests of honor, loyalty, and cosmic duty (Dharma)'},
                {'icon': 'fas fa-heart', 'title': 'Universal Catharsis', 'detail': 'Emotional resonance that bridges ancient centuries with contemporary life'}
            ],
            'workshop_stages': [
                {'step': '01', 'title': 'Invocation (Mangal)', 'desc': 'Opening prayers invoking blessings on the listeners and honoring ancient bards.'},
                {'step': '02', 'title': 'The Call to Adventure', 'desc': 'Setting the scene in ancient kingdoms, forests, or bustling trade routes.'},
                {'step': '03', 'title': 'Climax & Trial', 'desc': 'The supreme trial testing the protagonist\'s commitment to truth and devotion.'},
                {'step': '04', 'title': 'Resolution & Lesson', 'desc': 'The timeless moral takeaway imparted to the gathering around the hearth.'}
            ],
            'where_to_experience': [
                {'place': 'Folk Theatre Gatherings', 'city': f'{entry.state.name}', 'desc': 'Night-time community recitations under banyan trees and village squares.'},
                {'place': 'Heritage Literary Festivals', 'city': f'{entry.state.name}', 'desc': 'Panel discussions and oral storytelling sessions by contemporary folklorists.'},
                {'place': 'Regional Library Archives', 'city': f'{entry.state.name}', 'desc': 'Manuscript collections preserving illuminated palm leaves and oral transcripts.'}
            ],
            'curator_facts': [
                {'title': 'Living Oral Tradition', 'fact': f'{entry.title} has traveled across centuries primarily through the memory of traveling bards and grandmothers.'},
                {'title': 'Ethical North Star', 'fact': 'Folktales functioned as moral compasses for agrarian and nomadic societies.'},
                {'title': 'Regional Variations', 'fact': 'Different districts have their own unique colloquial versions and songs celebrating the tale.'}
            ],
            'quiz': {
                'question': f'How were stories like {entry.title} historically preserved across centuries?',
                'options': ['Generational Oral Storytelling', 'Printed Newspaper Columns', 'Radio Broadcasts', 'Digital Audio Recordings'],
                'correct_index': 0,
                'explanation': 'Generational oral transmission through wandering bards and family storytellers kept these epics vibrant for generations!'
            }
        }

def cultural_entry_detail(request, slug):
    entry = get_object_or_404(CulturalEntry.objects.prefetch_related('media_items'), slug=slug, status='published')
    connections = CulturalConnection.objects.filter(source_entry=entry) | CulturalConnection.objects.filter(target_entry=entry)
    
    media = entry.media_items.filter(is_active=True)
    images = media.filter(media_type='image').order_by('display_order')
    videos = media.filter(media_type='video').order_by('display_order')
    audios = media.filter(media_type='audio').order_by('display_order')
    
    is_favorite = False
    user_journeys = []
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, cultural_entry=entry).exists()
        user_journeys = CulturalJourney.objects.filter(user=request.user)
        
    experience_guide = get_experience_metadata(entry)
    
    return render(request, 'culture/cultural_entry.html', {
        'entry': entry,
        'connections': connections[:3],
        'is_favorite': is_favorite,
        'user_journeys': user_journeys,
        'images': images,
        'videos': videos,
        'audios': audios,
        'experience_guide': experience_guide,
    })

def cultural_connections(request, slug):
    entry = get_object_or_404(CulturalEntry, slug=slug, status='published')
    source_conns = CulturalConnection.objects.filter(source_entry=entry).select_related('target_entry', 'target_entry__state', 'target_entry__category')
    target_conns = CulturalConnection.objects.filter(target_entry=entry).select_related('source_entry', 'source_entry__state', 'source_entry__category')
    
    # Also fetch other cultural entries in the same state
    state_peers = CulturalEntry.objects.filter(state=entry.state, status='published').exclude(id=entry.id)[:4]
    
    # Also fetch entries in the same category from other states (e.g. other Martial/Dances)
    category_peers = CulturalEntry.objects.filter(category=entry.category, status='published').exclude(state=entry.state)[:4]
    
    total_connections_count = source_conns.count() + target_conns.count()
    
    return render(request, 'culture/connections.html', {
        'entry': entry,
        'source_conns': source_conns,
        'target_conns': target_conns,
        'state_peers': state_peers,
        'category_peers': category_peers,
        'total_connections_count': total_connections_count,
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

from culture.models import CulturalCalendarEvent, CulturalCategory, CulturalEntry, LiteraryWork

def cultural_calendar(request):
    events = CulturalCalendarEvent.objects.all().order_by('date')
    return render(request, 'exploration/calendar.html', {'events': events})

def museum(request):
    halls = CulturalCategory.objects.all().order_by('name')
    selected_hall_slug = request.GET.get('hall', '').strip()
    selected_hall = None
    hall_entries = []
    hall_works = []
    hall_festivals = []
    hall_cuisines = []
    hall_traditions = []
    
    if selected_hall_slug:
        selected_hall = CulturalCategory.objects.filter(slug=selected_hall_slug).first()
        if selected_hall:
            hall_entries = CulturalEntry.objects.filter(status='published', category=selected_hall)
            hall_works = LiteraryWork.objects.filter(status='published', category=selected_hall)
            if selected_hall_slug == 'festival':
                hall_festivals = Festival.objects.all()[:12]
            elif selected_hall_slug == 'cuisine':
                hall_cuisines = Cuisine.objects.all()[:12]
            elif selected_hall_slug == 'tradition':
                hall_traditions = Tradition.objects.all()[:12]

    featured_artifacts = CulturalEntry.objects.filter(status='published', featured=True)[:6]
    featured_manuscripts = LiteraryWork.objects.filter(status='published', featured=True)[:6]
    
    return render(request, 'exploration/museum.html', {
        'halls': halls,
        'selected_hall': selected_hall,
        'selected_hall_slug': selected_hall_slug,
        'hall_entries': hall_entries,
        'hall_works': hall_works,
        'hall_festivals': hall_festivals,
        'hall_cuisines': hall_cuisines,
        'hall_traditions': hall_traditions,
        'featured': featured_artifacts,
        'featured_manuscripts': featured_manuscripts,
    })


def digital_library(request):
    works = LiteraryWork.objects.filter(status='published')
    
    q = request.GET.get('q', '').strip()
    work_type = request.GET.get('type', '').strip()
    language = request.GET.get('language', '').strip()
    tradition = request.GET.get('tradition', '').strip()
    state_slug = request.GET.get('state', '').strip()
    classification = request.GET.get('classification', '').strip()
    
    if q:
        works = works.filter(
            Q(title__icontains=q) |
            Q(author_creator__icontains=q) |
            Q(synopsis__icontains=q) |
            Q(cultural_significance__icontains=q) |
            Q(language__icontains=q) |
            Q(tradition__icontains=q)
        )
    if work_type:
        works = works.filter(work_type=work_type)
    if language:
        works = works.filter(language__icontains=language)
    if tradition:
        works = works.filter(tradition__icontains=tradition)
    if state_slug:
        works = works.filter(state__slug=state_slug)
    if classification:
        works = works.filter(classification_type=classification)
        
    languages = LiteraryWork.objects.filter(status='published').values_list('language', flat=True).distinct()
    all_states = State.objects.all().order_by('name')
    
    return render(request, 'exploration/library.html', {
        'works': works,
        'work_types': LiteraryWork.WORK_TYPE_CHOICES,
        'classifications': LiteraryWork.CLASSIFICATION_CHOICES,
        'languages': sorted(list(set(languages))),
        'states': all_states,
        'selected_q': q,
        'selected_type': work_type,
        'selected_language': language,
        'selected_tradition': tradition,
        'selected_state': state_slug,
        'selected_classification': classification,
        'total_count': works.count(),
    })

def library_detail(request, slug):
    work = get_object_or_404(LiteraryWork, slug=slug, status='published')
    related_entries = work.related_entries.filter(status='published')
    
    # Cross-references in same tradition or language
    sibling_works = LiteraryWork.objects.filter(status='published').exclude(id=work.id).filter(
        Q(tradition__icontains=work.tradition) | Q(language__iexact=work.language)
    )[:4]
    
    return render(request, 'exploration/library_detail.html', {
        'work': work,
        'related_entries': related_entries,
        'sibling_works': sibling_works,
    })

def knowledge_graph(request, state_slug=None):
    selected_state = None
    if state_slug:
        selected_state = get_object_or_404(State, slug=state_slug)
        
    state_filter = request.GET.get('state', '').strip()
    if not selected_state and state_filter:
        selected_state = State.objects.filter(slug=state_filter).first()
        
    category_filter = request.GET.get('category', '').strip()
    search_q = request.GET.get('q', '').strip()
    
    # Fetch base entries
    entries_qs = CulturalEntry.objects.filter(status='published').select_related('state', 'category')
    works_qs = LiteraryWork.objects.filter(status='published').select_related('state', 'category')
    
    if selected_state:
        entries_qs = entries_qs.filter(state=selected_state)
        works_qs = works_qs.filter(Q(state=selected_state) | Q(state__isnull=True))
        
    if category_filter:
        entries_qs = entries_qs.filter(category__slug=category_filter)
        works_qs = works_qs.filter(category__slug=category_filter)
        
    if search_q:
        entries_qs = entries_qs.filter(Q(title__icontains=search_q) | Q(short_description__icontains=search_q))
        works_qs = works_qs.filter(Q(title__icontains=search_q) | Q(author_creator__icontains=search_q))

    # Limit nodes to avoid overloading browser canvas while keeping high density
    active_entries = list(entries_qs[:45])
    active_entry_ids = set(e.id for e in active_entries)
    active_works = list(works_qs[:15])
    
    nodes = []
    edges = []
    node_ids = set()
    
    # Category color tokens
    cat_colors = {
        'dance': '#f43f5e',
        'music': '#6366f1',
        'craft': '#10b981',
        'cuisine': '#f59e0b',
        'festival': '#f97316',
        'story': '#8b5cf6',
        'literature': '#0284c7',
        'sacred-texts': '#d97706',
        'manuscripts': '#7c3aed',
        'oral-tradition': '#ec4899',
        'traditional-knowledge': '#059669',
        'state': '#1e293b'
    }
    
    # If state selected, add State as central hub node
    if selected_state:
        state_node_id = f"state_{selected_state.id}"
        nodes.append({
            'id': state_node_id,
            'label': selected_state.name,
            'type': 'State Hub',
            'category': 'state',
            'color': '#ff9933',
            'radius': 28,
            'summary': selected_state.cultural_summary or selected_state.description[:120],
            'url': f"/explore/states/{selected_state.slug}/"
        })
        node_ids.add(state_node_id)
        
    # Add Cultural Entries as Nodes
    for e in active_entries:
        n_id = f"entry_{e.id}"
        c_slug = e.category.slug
        color = cat_colors.get(c_slug, '#3b82f6')
        nodes.append({
            'id': n_id,
            'label': e.title,
            'type': e.category.name,
            'category': c_slug,
            'color': color,
            'radius': 18,
            'summary': (e.short_description[:130] + '...') if len(e.short_description) > 130 else e.short_description,
            'state': e.state.name,
            'url': f"/explore/culture/{e.slug}/"
        })
        node_ids.add(n_id)
        
        # Link entry to central State node
        if selected_state:
            edges.append({
                'source': f"state_{selected_state.id}",
                'target': n_id,
                'label': 'Indigenous Living Tradition',
                'description': f"Part of the cultural heritage matrix of {selected_state.name}"
            })

    # Add Literary Works as Nodes
    for w in active_works:
        w_id = f"work_{w.id}"
        c_slug = w.category.slug if w.category else 'literature'
        color = cat_colors.get(c_slug, '#0284c7')
        nodes.append({
            'id': w_id,
            'label': w.title,
            'type': w.get_work_type_display(),
            'category': c_slug,
            'color': color,
            'radius': 20,
            'summary': w.brief_intro[:130] if w.brief_intro else w.synopsis[:130],
            'state': w.state.name if w.state else 'Pan-Indian',
            'url': f"/library/{w.slug}/"
        })
        node_ids.add(w_id)
        
        if selected_state and w.state == selected_state:
            edges.append({
                'source': f"state_{selected_state.id}",
                'target': w_id,
                'label': 'Regional Literary Heritage',
                'description': f"Classic literary / philosophical canon of {selected_state.name}"
            })
            
        # Add edges between work and related cultural entries
        for rel_entry in w.related_entries.filter(status='published'):
            rel_id = f"entry_{rel_entry.id}"
            if rel_id in node_ids:
                edges.append({
                    'source': w_id,
                    'target': rel_id,
                    'label': 'Literary Inspiration / Motif',
                    'description': f"{w.title} depicts and shares narrative motifs with {rel_entry.title}"
                })

    # Fetch Cultural Connections between active entries
    if active_entry_ids:
        conns = CulturalConnection.objects.filter(
            Q(source_entry_id__in=active_entry_ids) | Q(target_entry_id__in=active_entry_ids)
        ).select_related('source_entry', 'target_entry', 'source_entry__category', 'target_entry__category')
        
        for c in conns:
            s_id = f"entry_{c.source_entry_id}"
            t_id = f"entry_{c.target_entry_id}"
            
            # If target entry is not in active nodes, add it if capacity allows
            if t_id not in node_ids and len(nodes) < 70:
                te = c.target_entry
                nodes.append({
                    'id': t_id,
                    'label': te.title,
                    'type': te.category.name,
                    'category': te.category.slug,
                    'color': cat_colors.get(te.category.slug, '#3b82f6'),
                    'radius': 14,
                    'summary': te.short_description[:120],
                    'state': te.state.name,
                    'url': f"/explore/culture/{te.slug}/"
                })
                node_ids.add(t_id)
                
            if s_id in node_ids and t_id in node_ids:
                edges.append({
                    'source': s_id,
                    'target': t_id,
                    'label': c.relationship_type,
                    'description': c.description or f"Direct verified cultural connection between {c.source_entry.title} and {c.target_entry.title}"
                })

    all_states = State.objects.all().order_by('name')
    categories = CulturalCategory.objects.all().order_by('name')

    return render(request, 'exploration/knowledge_graph.html', {
        'selected_state': selected_state,
        'all_states': all_states,
        'categories': categories,
        'category_filter': category_filter,
        'search_q': search_q,
        'nodes_json': json.dumps(nodes),
        'edges_json': json.dumps(edges),
        'nodes_count': len(nodes),
        'edges_count': len(edges),
        'nodes_list': nodes,
    })


