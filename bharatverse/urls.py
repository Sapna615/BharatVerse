from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, global_search, privacy_policy, terms_of_service, ai_guidelines
from exploration.views import digital_library, library_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search/', global_search, name='global_search'),
    path('privacy/', privacy_policy, name='privacy_policy'),
    path('terms/', terms_of_service, name='terms_of_service'),
    path('ai-guidelines/', ai_guidelines, name='ai_guidelines'),
    path('library/', digital_library, name='root_digital_library'),
    path('library/<slug:slug>/', library_detail, name='root_library_detail'),
    path('journey/', include('journeys.urls')),
    path('accounts/', include('accounts.urls')),
    path('explore/', include('exploration.urls')),
    path('api/', include('culture.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('games/', include('games.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('gamification/', include('gamification.urls')),
    path('contribute/', include('contributions.urls')),
]

from django.views.static import serve
import re

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
