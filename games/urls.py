from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_hub, name='games_hub'),
    path('puzzle/<slug:slug>/', views.play_puzzle, name='play_puzzle'),
    path('word-search/<slug:slug>/', views.play_word_search, name='play_word_search'),
    path('crossword/<slug:slug>/', views.play_crossword, name='play_crossword'),
    path('<slug:slug>/', views.game_detail, name='game_detail'),
]
