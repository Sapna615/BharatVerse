from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, global_search
from exploration.views import digital_library, library_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search/', global_search, name='global_search'),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
