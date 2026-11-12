from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Game
from culture.models import State, CulturalCategory

def games_hub(request):
    games = Game.objects.filter(is_active=True).order_by('-created_at')
    
    # Optional filters
    game_type = request.GET.get('type')
    state_id = request.GET.get('state')
    category_id = request.GET.get('category')
    search = request.GET.get('q')
    
    if game_type:
        games = games.filter(game_type=game_type)
    if state_id:
        games = games.filter(state_id=state_id)
    if category_id:
        games = games.filter(category_id=category_id)
    if search:
        games = games.filter(title__icontains=search)
        
    states = State.objects.all().order_by('name')
    categories = CulturalCategory.objects.all().order_by('name')
        
    return render(request, 'games/hub.html', {
        'games': games,
        'states': states,
        'categories': categories,
        'game_types': Game.GAME_TYPES,
        'selected_type': game_type,
        'selected_state': state_id,
        'selected_category': category_id,
        'search_query': search
    })

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug, is_active=True)
    return render(request, 'games/detail.html', {'game': game})

def play_puzzle(request, slug):
    game = get_object_or_404(Game, slug=slug, is_active=True, game_type='picture_puzzle')
    
    # We can pass difficulty from the request, default to easy (3x3)
    difficulty = request.GET.get('difficulty', 'easy')
    grid_size = 3
    if difficulty == 'medium':
        grid_size = 4
    elif difficulty == 'hard':
        grid_size = 5
        
    return render(request, 'games/play_puzzle.html', {
        'game': game,
        'difficulty': difficulty,
        'grid_size': grid_size
    })

def play_word_search(request, slug):
    game = get_object_or_404(Game, slug=slug, is_active=True, game_type='word_search')
    difficulty = request.GET.get('difficulty', 'easy')
    
    # Normally we would fetch words from a related model, but for now we pass a list
    # associated with the game's category or title.
    words = []
    
    # Check specific slugs first for most relevant context
    if 'literature' in slug.lower():
        words = ['RAMAYANA', 'SILAPPADIKARAM', 'GITANJALI', 'THIRUKKURAL', 'JATAKA', 'HEER', 'BULLEH', 'TAGORE']
    elif 'punjab' in slug.lower():
        words = ['PUNJAB', 'BHANGRA', 'GIDDHA', 'AMRITSAR', 'LOHRI', 'BAISAKHI', 'PHULKARI', 'SARSON']
    elif game.category and game.category.name.lower() == 'dance':
        words = ['BHARATNATYAM', 'KATHAK', 'ODISSI', 'KATHAKALI', 'KUCHIPUDI', 'MANIPURI', 'MOHINIYATTAM', 'SATTRIYA']
    elif game.category and game.category.name.lower() == 'festival':
        words = ['DIWALI', 'HOLI', 'DUSSEHRA', 'NAVRATRI', 'EID', 'CHRISTMAS', 'PONGAL', 'ONAM', 'BAISAKHI']
    elif game.state:
        words = [game.state.name.upper(), 'CAPITAL', 'CULTURE', 'HERITAGE', 'INDIA', 'TRADITION']
    else:
        words = ['HERITAGE', 'CULTURE', 'INDIA', 'TRADITION', 'HISTORY', 'DIVERSITY', 'UNITY', 'PEACE']

    # Grid sizes: easy=10x10, medium=12x12, hard=15x15
    grid_size = 10
    if difficulty == 'medium':
        grid_size = 12
    elif difficulty == 'hard':
        grid_size = 15
        
    # Ensure grid is at least as large as the longest word + 2 for padding
    if words:
        max_word_len = max(len(w) for w in words)
        if max_word_len + 2 > grid_size:
            grid_size = max_word_len + 2

    import json
    return render(request, 'games/play_word_search.html', {
        'game': game,
        'difficulty': difficulty,
        'grid_size': grid_size,
        'words_json': json.dumps(words),
        'words': words
    })

def play_crossword(request, slug):
    game = get_object_or_404(Game, slug=slug, is_active=True, game_type='crossword')
    
    # Check if this is the literary crossword
    if 'author' in slug.lower() or 'literature' in slug.lower():
        crossword_data = [
            {"word": "TAGORE", "clue": "Bengali poet who composed Gitanjali and won the 1913 Nobel Prize", "start_row": 1, "start_col": 1, "direction": "across", "number": 1},
            {"word": "TULSI", "clue": "Saint-poet who composed Ramcharitmanas in Awadhi", "start_row": 1, "start_col": 1, "direction": "down", "number": 1},
            {"word": "KURAL", "clue": "Sacred Tamil couplets on ethics by Thiruvalluvar", "start_row": 3, "start_col": 4, "direction": "across", "number": 2},
            {"word": "ILANGO", "clue": "Chera prince-author of the epic Silappadikaram", "start_row": 2, "start_col": 6, "direction": "down", "number": 3},
            {"word": "PALI", "clue": "Ancient language in which the Jataka tales were preserved", "start_row": 6, "start_col": 2, "direction": "across", "number": 4},
        ]
    else:
        crossword_data = [
            {"word": "DIWALI", "clue": "Festival of lights", "start_row": 1, "start_col": 1, "direction": "across", "number": 1},
            {"word": "DHARMA", "clue": "Cosmic law and order", "start_row": 1, "start_col": 1, "direction": "down", "number": 1},
            {"word": "AGRA", "clue": "City of the Taj Mahal", "start_row": 3, "start_col": 5, "direction": "across", "number": 2},
            {"word": "RAMAYANA", "clue": "Ancient Indian epic", "start_row": 3, "start_col": 7, "direction": "down", "number": 3},
            {"word": "YOGA", "clue": "Ancient physical and mental discipline", "start_row": 7, "start_col": 7, "direction": "across", "number": 4},
        ]
    
    import json
    return render(request, 'games/play_crossword.html', {
        'game': game,
        'difficulty': 'easy',
        'grid_width': 12,
        'grid_height': 12,
        'words_json': json.dumps(crossword_data),
        'total_words': len(crossword_data)
    })

