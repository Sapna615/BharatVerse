from django.urls import path
from .views import dashboard, quests_list, achievements_list

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('quests/', quests_list, name='quests_list'),
    path('achievements/', achievements_list, name='achievements_list'),
]
