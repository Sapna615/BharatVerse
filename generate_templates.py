import os

BASE_DIR = '/Users/sapnarai/BharatVerse'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}BharatVerse - Discover India{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        bharat: {
                            navy: '#1A2942',
                            amber: '#D4AF37',
                            saffron: '#FF9933',
                            cream: '#FDFBF7',
                            charcoal: '#333333'
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        serif: ['Merriweather', 'serif']
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Merriweather:wght@400;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #FDFBF7; color: #333333; }
        h1, h2, h3, h4, h5, h6 { font-family: 'Merriweather', serif; }
        .glass-panel { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); }
    </style>
</head>
<body class="flex flex-col min-h-screen">
    {% include 'partials/navbar.html' %}
    
    <main class="flex-grow">
        {% if messages %}
        <div class="max-w-7xl mx-auto px-4 mt-4">
            {% for message in messages %}
            <div class="p-4 mb-4 text-sm rounded-lg {% if message.tags == 'error' %}bg-red-100 text-red-700{% else %}bg-green-100 text-green-700{% endif %}" role="alert">
                {{ message }}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>

    {% include 'partials/footer.html' %}
</body>
</html>
"""

navbar_html = """<nav class="bg-bharat-navy text-white shadow-lg sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
            <div class="flex">
                <a href="/" class="flex-shrink-0 flex items-center gap-2">
                    <span class="text-2xl font-serif text-bharat-saffron font-bold">BharatVerse</span>
                </a>
                <div class="hidden sm:ml-6 sm:flex sm:space-x-8 items-center">
                    <a href="#" class="border-transparent text-gray-300 hover:text-white hover:border-gray-300 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Explore India</a>
                    <a href="#" class="border-transparent text-gray-300 hover:text-white hover:border-gray-300 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Cultural Map</a>
                    <a href="#" class="border-transparent text-gray-300 hover:text-white hover:border-gray-300 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">BharatVerse AI</a>
                </div>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:items-center space-x-4">
                {% if user.is_authenticated %}
                    <a href="#" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Dashboard</a>
                    <form method="post" action="{% url 'logout' %}">
                        {% csrf_token %}
                        <button type="submit" class="text-bharat-saffron hover:text-white px-3 py-2 rounded-md text-sm font-medium">Logout</button>
                    </form>
                {% else %}
                    <a href="{% url 'login' %}" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Sign in</a>
                    <a href="{% url 'register' %}" class="bg-bharat-amber text-bharat-navy hover:bg-yellow-500 px-4 py-2 rounded-md text-sm font-bold shadow-md transition">Register</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
"""

footer_html = """<footer class="bg-bharat-navy text-gray-300 mt-12 py-8 border-t border-gray-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-center">
            <div class="mb-4 md:mb-0">
                <span class="text-xl font-serif text-bharat-saffron font-bold block">BharatVerse</span>
                <span class="text-sm">Discover India. Experience Culture. Preserve Heritage.</span>
            </div>
            <div class="flex space-x-6 text-sm">
                <a href="#" class="hover:text-white transition">About</a>
                <a href="#" class="hover:text-white transition">Terms</a>
                <a href="#" class="hover:text-white transition">Privacy</a>
            </div>
        </div>
        <div class="mt-8 text-center text-xs text-gray-500">
            &copy; 2026 BharatVerse - SIH26197. All rights reserved.
        </div>
    </div>
</footer>
"""

home_html = """{% extends 'base.html' %}

{% block title %}BharatVerse - Home{% endblock %}

{% block content %}
<div class="relative bg-bharat-navy overflow-hidden">
    <!-- Background visual -->
    <div class="absolute inset-0 z-0 opacity-20">
        <div class="w-full h-full bg-gradient-to-br from-bharat-saffron to-bharat-navy"></div>
    </div>
    
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 text-center">
        <h1 class="text-5xl md:text-7xl font-serif font-bold text-white mb-6 drop-shadow-md">
            One India. <span class="text-bharat-amber">Thousands of Stories.</span>
        </h1>
        <p class="mt-4 text-xl text-gray-200 max-w-3xl mx-auto mb-10 font-light">
            Discover the traditions, art, stories, food, festivals and living heritage that make India extraordinary.
        </p>
        <div class="flex justify-center gap-4">
            <a href="#" class="bg-bharat-saffron hover:bg-orange-600 text-white font-bold py-3 px-8 rounded-full shadow-lg transition transform hover:-translate-y-1">
                Explore India
            </a>
            <a href="#" class="bg-transparent border-2 border-bharat-amber text-bharat-amber hover:bg-bharat-amber hover:text-bharat-navy font-bold py-3 px-8 rounded-full shadow-lg transition">
                Start My Cultural Journey
            </a>
        </div>
    </div>
</div>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <h2 class="text-3xl font-serif text-center mb-12 text-bharat-navy">Explore by Region</h2>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {% for region in regions %}
        <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition p-6 text-center cursor-pointer border border-gray-100 hover:border-bharat-saffron">
            <h3 class="font-bold text-bharat-navy">{{ region }}</h3>
        </div>
        {% endfor %}
    </div>
</div>

<div class="bg-white py-16 border-t border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-serif text-center mb-12 text-bharat-navy">Featured Heritage</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {% for entry in featured_entries %}
            <div class="rounded-2xl overflow-hidden shadow-lg border border-gray-100 bg-bharat-cream group">
                <div class="h-48 bg-gray-200 w-full relative overflow-hidden">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                    <span class="absolute bottom-4 left-4 text-white font-bold">{{ entry.category.name }}</span>
                </div>
                <div class="p-6">
                    <div class="text-xs text-bharat-saffron font-bold uppercase tracking-wider mb-2">{{ entry.state.name }}</div>
                    <h3 class="text-xl font-serif font-bold text-bharat-navy mb-2">{{ entry.title }}</h3>
                    <p class="text-gray-600 text-sm mb-4 line-clamp-3">{{ entry.short_description }}</p>
                    <a href="#" class="text-bharat-amber font-semibold hover:text-yellow-600">Read Cultural Story &rarr;</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
"""

files = {
    'base.html': base_html,
    'partials/navbar.html': navbar_html,
    'partials/footer.html': footer_html,
    'home.html': home_html,
}

for path, content in files.items():
    with open(os.path.join(TEMPLATES_DIR, path), 'w') as f:
        f.write(content)
    print(f"Generated {path}")
