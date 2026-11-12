from django.urls import path
from .views import (explore_india, cultural_map, state_detail, 
                    cultural_entry_detail, cultural_connections,
                    toggle_favorite, add_to_journey, compare_cultures, favorites_list, cultural_calendar, museum,
                    digital_library, library_detail, knowledge_graph)

urlpatterns = [
    path('', explore_india, name='explore_india'),
    path('map/', cultural_map, name='cultural_map'),
    path('knowledge-graph/', knowledge_graph, name='knowledge_graph'),
    path('knowledge-graph/<slug:state_slug>/', knowledge_graph, name='state_knowledge_graph'),
    path('library/', digital_library, name='digital_library'),
    path('library/<slug:slug>/', library_detail, name='library_detail'),
    path('states/<slug:slug>/', state_detail, name='state_detail'),
    path('culture/<slug:slug>/', cultural_entry_detail, name='cultural_entry_detail'),
    path('connections/<slug:slug>/', cultural_connections, name='cultural_connections'),
    path('culture/<slug:slug>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('culture/<slug:slug>/add-to-journey/', add_to_journey, name='add_to_journey'),

    path('compare/', compare_cultures, name='compare_cultures'),
    path('favorites/', favorites_list, name='favorites_list'),

    path('calendar/', cultural_calendar, name='cultural_calendar'),
    path('museum/', museum, name='museum'),
]


