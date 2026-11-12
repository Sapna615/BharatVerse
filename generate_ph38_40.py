import os

BASE_DIR = '/Users/sapnarai/BharatVerse'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# --- 1. Exploration Views for Calendar and Museum ---
exploration_views_addition = """
from culture.models import CulturalCalendarEvent, CulturalCategory, CulturalEntry

def cultural_calendar(request):
    events = CulturalCalendarEvent.objects.all().order_by('date')
    return render(request, 'exploration/calendar.html', {'events': events})

def museum(request):
    halls = CulturalCategory.objects.all()
    featured_artifacts = CulturalEntry.objects.filter(status='published', featured=True)[:3]
    return render(request, 'exploration/museum.html', {'halls': halls, 'featured': featured_artifacts})
"""
with open(os.path.join(BASE_DIR, 'exploration', 'views.py'), 'a') as f:
    f.write(exploration_views_addition)

# Exploration URLs update
exploration_urls_addition = """
    path('calendar/', cultural_calendar, name='cultural_calendar'),
    path('museum/', museum, name='museum'),
"""
with open(os.path.join(BASE_DIR, 'exploration', 'urls.py'), 'r') as f:
    urls_content = f.read()

urls_content = urls_content.replace(
    'from .views import (explore_india, cultural_map, state_detail, \n                    cultural_entry_detail, cultural_connections,\n                    toggle_favorite, add_to_journey, compare_cultures, favorites_list)',
    'from .views import (explore_india, cultural_map, state_detail, \n                    cultural_entry_detail, cultural_connections,\n                    toggle_favorite, add_to_journey, compare_cultures, favorites_list, cultural_calendar, museum)'
)
urls_content = urls_content.replace(']', exploration_urls_addition + ']')
with open(os.path.join(BASE_DIR, 'exploration', 'urls.py'), 'w') as f:
    f.write(urls_content)


# --- 2. AI Assistant App ---
ai_views = """from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import AIService

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            ai = AIService()
            response_text = ai.ask_cultural_question(message)
            
            return JsonResponse({
                'success': True,
                'mode': 'demo' if ai.demo_mode else 'live',
                'message': response_text,
                'sources': ['BharatVerse Knowledge Base']
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
"""
with open(os.path.join(BASE_DIR, 'ai_assistant', 'views.py'), 'w') as f:
    f.write(ai_views)

ai_urls = """from django.urls import path
from .views import ai_chat

urlpatterns = [
    path('chat/', ai_chat, name='ai_chat'),
]
"""
with open(os.path.join(BASE_DIR, 'ai_assistant', 'urls.py'), 'w') as f:
    f.write(ai_urls)

with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'r') as f:
    bv_urls = f.read()
if "'ai_assistant.urls'" not in bv_urls:
    bv_urls = bv_urls.replace(
        "path('quizzes/', include('quizzes.urls')),",
        "path('quizzes/', include('quizzes.urls')),\n    path('api/ai/', include('ai_assistant.urls')),"
    )
    with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'w') as f:
        f.write(bv_urls)


# --- 3. Templates ---

calendar_html = """{% extends 'base.html' %}
{% block title %}Cultural Calendar - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">India's Cultural Calendar</h1>
    <p class="text-gray-300 font-light">Festivals, traditions, celebrations, and cultural moments across India.</p>
</div>

<div class="max-w-6xl mx-auto px-4 py-16">
    <div class="flex justify-between items-center mb-8">
        <h2 class="text-2xl font-bold text-bharat-navy">Coming Up</h2>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        {% for e in events|slice:":3" %}
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col hover:shadow-md transition">
            <span class="text-xs font-bold text-bharat-saffron uppercase mb-1">{{ e.month }}</span>
            <h3 class="text-lg font-bold text-bharat-navy mb-2">{{ e.name }}</h3>
            <p class="text-sm text-gray-600 mb-4 flex-grow">{{ e.description|truncatewords:20 }}</p>
            <a href="#" class="text-sm font-bold text-bharat-amber hover:text-yellow-600">Explore Culture &rarr;</a>
        </div>
        {% empty %}
        <div class="col-span-3 text-center text-gray-500 py-12">No upcoming events scheduled.</div>
        {% endfor %}
    </div>
    
    <h2 class="text-2xl font-bold text-bharat-navy mb-8">Full Calendar</h2>
    <div class="bg-white rounded-xl shadow border border-gray-200 overflow-hidden">
        <table class="w-full text-left text-sm">
            <thead class="bg-gray-50 border-b border-gray-200 text-gray-700">
                <tr>
                    <th class="p-4">Event</th>
                    <th class="p-4">Month/Date</th>
                    <th class="p-4">State</th>
                    <th class="p-4">Category</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                {% for e in events %}
                <tr class="hover:bg-gray-50 transition">
                    <td class="p-4 font-bold text-bharat-navy">{{ e.name }}</td>
                    <td class="p-4">{{ e.month }} {% if e.date %}{{ e.date|date:"d" }}{% endif %}</td>
                    <td class="p-4">{{ e.state.name|default:"Pan-India" }}</td>
                    <td class="p-4"><span class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">{{ e.category.name|default:"General" }}</span></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'exploration', 'calendar.html'), 'w') as f:
    f.write(calendar_html)

museum_html = """{% extends 'base.html' %}
{% block title %}Virtual Museum - BharatVerse{% endblock %}
{% block content %}
<div class="bg-gray-900 py-20 text-center relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-b from-black to-transparent opacity-50 z-0"></div>
    <div class="relative z-10 max-w-4xl mx-auto px-4">
        <span class="text-bharat-saffron font-bold tracking-widest uppercase text-sm mb-4 block">The BharatVerse Museum</span>
        <h1 class="text-5xl md:text-6xl font-serif font-bold text-white mb-6">Walk through India's living heritage.</h1>
        <p class="text-xl text-gray-400 font-light mb-8">Explore traditions, crafts, stories, music, dance, cuisine, clothing, and cultural memories.</p>
        <button class="bg-white text-gray-900 font-bold py-3 px-8 rounded-full shadow hover:bg-gray-200 transition">Enter the Museum</button>
    </div>
</div>

<div class="bg-bharat-navy py-16">
    <div class="max-w-7xl mx-auto px-4">
        <h2 class="text-3xl font-serif font-bold text-white mb-12 text-center border-b border-gray-700 pb-4 inline-block">Featured Artifacts</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {% for art in featured %}
            <div class="bg-gray-800 rounded-xl overflow-hidden border border-gray-700 group hover:border-bharat-amber transition">
                <div class="h-48 bg-gray-700 relative">
                    {% if art.image %}
                    <img src="{{ art.image.url }}" class="w-full h-full object-cover opacity-70 group-hover:opacity-100 transition">
                    {% endif %}
                    <div class="absolute bottom-4 left-4">
                        <span class="bg-bharat-amber text-bharat-navy text-xs font-bold px-2 py-1 rounded">{{ art.category.name }}</span>
                    </div>
                </div>
                <div class="p-6">
                    <div class="text-gray-400 text-sm mb-1">{{ art.state.name }}</div>
                    <h3 class="text-xl font-bold text-white mb-3">{{ art.title }}</h3>
                    <p class="text-gray-400 text-sm mb-4 line-clamp-3">{{ art.short_description }}</p>
                    <a href="{% url 'cultural_entry_detail' art.slug %}" class="text-white font-bold hover:text-bharat-saffron text-sm">Examine Artifact &rarr;</a>
                </div>
            </div>
            {% empty %}
            <p class="text-gray-500 text-center col-span-3">No featured artifacts available.</p>
            {% endfor %}
        </div>
    </div>
</div>

<div class="bg-gray-50 py-16">
    <div class="max-w-7xl mx-auto px-4">
        <h2 class="text-3xl font-serif font-bold text-bharat-navy mb-8 text-center">Museum Halls</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            {% for hall in halls %}
            <div class="bg-white border border-gray-200 rounded-xl p-6 text-center hover:shadow-lg transition cursor-pointer hover:border-bharat-navy">
                <div class="text-3xl mb-3">🏛️</div>
                <h3 class="font-bold text-gray-800">Hall of {{ hall.name }}s</h3>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'exploration', 'museum.html'), 'w') as f:
    f.write(museum_html)


# --- 4. Update Base Template with Floating AI ---
with open(os.path.join(TEMPLATES_DIR, 'base.html'), 'r') as f:
    base_html = f.read()

if "id=\"ai-chat-btn\"" not in base_html:
    ai_html = """
    <!-- Floating AI Assistant -->
    <button id="ai-chat-btn" onclick="toggleChat()" class="fixed bottom-6 right-6 bg-bharat-navy text-white rounded-full p-4 shadow-xl hover:bg-gray-800 hover:scale-105 transition-transform z-50 flex items-center justify-center border-2 border-bharat-amber">
        🤖 <span class="ml-2 font-bold hidden sm:inline">Ask AI</span>
    </button>

    <div id="ai-chat-panel" class="fixed bottom-24 right-6 w-80 sm:w-96 h-[500px] bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 flex flex-col hidden overflow-hidden">
        <!-- Header -->
        <div class="bg-bharat-navy p-4 text-white flex justify-between items-center">
            <div>
                <h3 class="font-serif font-bold text-lg">BharatVerse AI</h3>
                <p class="text-xs text-bharat-amber flex items-center"><span class="w-2 h-2 rounded-full bg-green-400 mr-1"></span> Ready to explore (Demo)</p>
            </div>
            <button onclick="toggleChat()" class="text-gray-400 hover:text-white">&times;</button>
        </div>
        
        <!-- Messages -->
        <div id="ai-messages" class="flex-grow p-4 overflow-y-auto space-y-4 bg-gray-50">
            <div class="bg-white p-3 rounded-lg rounded-tl-none shadow-sm border border-gray-100 max-w-[85%] text-sm text-gray-700">
                Namaste! I am your cultural guide. What would you like to explore in India today?
            </div>
            <div class="space-y-2">
                <button onclick="sendMsg('Tell me about a traditional art form from Rajasthan.')" class="text-xs bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-full px-3 py-1 hover:bg-indigo-100 block text-left">Tell me about art from Rajasthan</button>
                <button onclick="sendMsg('Explain Diwali simply.')" class="text-xs bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-full px-3 py-1 hover:bg-indigo-100 block text-left">Explain Diwali simply</button>
            </div>
        </div>
        
        <!-- Input -->
        <div class="p-4 bg-white border-t border-gray-100">
            <div class="flex">
                <input type="text" id="ai-input" placeholder="Ask a cultural question..." class="flex-grow border-gray-300 rounded-l-lg text-sm focus:ring-bharat-saffron focus:border-bharat-saffron" onkeypress="if(event.key === 'Enter') sendInput()">
                <button onclick="sendInput()" class="bg-bharat-saffron text-white px-4 rounded-r-lg hover:bg-orange-600">Send</button>
            </div>
        </div>
    </div>

    <script>
        function toggleChat() {
            const panel = document.getElementById('ai-chat-panel');
            panel.classList.toggle('hidden');
        }
        
        function appendMsg(text, isUser=false) {
            const msgs = document.getElementById('ai-messages');
            const div = document.createElement('div');
            div.className = isUser 
                ? "bg-bharat-saffron text-white p-3 rounded-lg rounded-tr-none shadow-sm max-w-[85%] text-sm self-end ml-auto"
                : "bg-white p-3 rounded-lg rounded-tl-none shadow-sm border border-gray-100 max-w-[85%] text-sm text-gray-700";
            
            // Format line breaks for AI response
            if (!isUser) {
                div.innerHTML = text.replace(/\\n/g, '<br>');
            } else {
                div.innerText = text;
            }
            
            msgs.appendChild(div);
            msgs.scrollTop = msgs.scrollHeight;
        }

        async function sendMsg(text) {
            appendMsg(text, true);
            const msgs = document.getElementById('ai-messages');
            
            // Loading
            const loading = document.createElement('div');
            loading.className = "text-xs text-gray-400 italic";
            loading.id = "ai-loading";
            loading.innerText = "Thinking...";
            msgs.appendChild(loading);
            
            try {
                const response = await fetch('/api/ai/chat/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await response.json();
                document.getElementById('ai-loading').remove();
                
                if (data.success) {
                    appendMsg(data.message, false);
                } else {
                    appendMsg("Sorry, an error occurred.", false);
                }
            } catch (e) {
                document.getElementById('ai-loading').remove();
                appendMsg("Sorry, connection failed.", false);
            }
        }
        
        function sendInput() {
            const input = document.getElementById('ai-input');
            if (input.value.trim() !== '') {
                sendMsg(input.value);
                input.value = '';
            }
        }
    </script>
"""
    base_html = base_html.replace('</body>', ai_html + '\n</body>')
    with open(os.path.join(TEMPLATES_DIR, 'base.html'), 'w') as f:
        f.write(base_html)
