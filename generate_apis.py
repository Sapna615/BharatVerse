import os

BASE_DIR = '/Users/sapnarai/BharatVerse'

culture_serializers = """from rest_framework import serializers
from .models import State, CulturalCategory, CulturalEntry, Festival, Tradition, FolkArt, Cuisine, CulturalConnection, CulturalCalendarEvent

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CulturalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalCategory
        fields = '__all__'

class CulturalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalEntry
        fields = '__all__'

class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival
        fields = '__all__'

class TraditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tradition
        fields = '__all__'

class FolkArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolkArt
        fields = '__all__'

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = '__all__'

class CulturalConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalConnection
        fields = '__all__'

class CulturalCalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalCalendarEvent
        fields = '__all__'
"""

culture_views = """from rest_framework import viewsets, permissions
from .models import State, CulturalCategory, CulturalEntry, Festival, Tradition, FolkArt, Cuisine, CulturalConnection, CulturalCalendarEvent
from .serializers import (StateSerializer, CulturalCategorySerializer, CulturalEntrySerializer, 
                          FestivalSerializer, TraditionSerializer, FolkArtSerializer, 
                          CuisineSerializer, CulturalConnectionSerializer, CulturalCalendarEventSerializer)
from rest_framework.decorators import action
from rest_framework.response import Response

class ReadOnlyOrAdminPermission(permissions.IsAuthenticatedOrReadOnly):
    pass

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    lookup_field = 'slug'
    permission_classes = [ReadOnlyOrAdminPermission]

    @action(detail=True, methods=['get'])
    def fingerprint(self, request, slug=None):
        state = self.get_object()
        # Simulated fingerprint calculation
        data = {
            "state": state.name,
            "dance": CulturalEntry.objects.filter(state=state, category__name='Dance').count(),
            "music": CulturalEntry.objects.filter(state=state, category__name='Music').count(),
            "craft": CulturalEntry.objects.filter(state=state, category__name='Craft').count(),
            "cuisine": Cuisine.objects.filter(state=state).count(),
            "festivals": Festival.objects.filter(state=state).count(),
        }
        return Response(data)

class CulturalCategoryViewSet(viewsets.ModelViewSet):
    queryset = CulturalCategory.objects.all()
    serializer_class = CulturalCategorySerializer
    lookup_field = 'slug'
    permission_classes = [ReadOnlyOrAdminPermission]

class CulturalEntryViewSet(viewsets.ModelViewSet):
    queryset = CulturalEntry.objects.filter(status='published')
    serializer_class = CulturalEntrySerializer
    lookup_field = 'slug'
    permission_classes = [ReadOnlyOrAdminPermission]

    @action(detail=True, methods=['get'])
    def connections(self, request, slug=None):
        entry = self.get_object()
        conns = CulturalConnection.objects.filter(source_entry=entry) | CulturalConnection.objects.filter(target_entry=entry)
        serializer = CulturalConnectionSerializer(conns, many=True)
        return Response(serializer.data)

class FestivalViewSet(viewsets.ModelViewSet):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    lookup_field = 'slug'
    permission_classes = [ReadOnlyOrAdminPermission]

class TraditionViewSet(viewsets.ModelViewSet):
    queryset = Tradition.objects.all()
    serializer_class = TraditionSerializer
    lookup_field = 'slug'
    permission_classes = [ReadOnlyOrAdminPermission]

class FolkArtViewSet(viewsets.ModelViewSet):
    queryset = FolkArt.objects.all()
    serializer_class = FolkArtSerializer
    lookup_field = 'slug'
    permission_classes = [ReadOnlyOrAdminPermission]

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    lookup_field = 'slug'
    permission_classes = [ReadOnlyOrAdminPermission]

class CulturalCalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CulturalCalendarEvent.objects.all()
    serializer_class = CulturalCalendarEventSerializer
    permission_classes = [ReadOnlyOrAdminPermission]
"""

culture_urls = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (StateViewSet, CulturalCategoryViewSet, CulturalEntryViewSet, 
                    FestivalViewSet, TraditionViewSet, FolkArtViewSet, 
                    CuisineViewSet, CulturalCalendarEventViewSet)

router = DefaultRouter()
router.register(r'states', StateViewSet)
router.register(r'categories', CulturalCategoryViewSet)
router.register(r'culture', CulturalEntryViewSet)
router.register(r'festivals', FestivalViewSet)
router.register(r'traditions', TraditionViewSet)
router.register(r'folk-arts', FolkArtViewSet)
router.register(r'cuisines', CuisineViewSet)
router.register(r'calendar', CulturalCalendarEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""

bharatverse_urls = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('culture.urls')),
    # Add other APIs when ready
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""

files = {
    'culture/serializers.py': culture_serializers,
    'culture/views.py': culture_views,
    'culture/urls.py': culture_urls,
    'bharatverse/urls.py': bharatverse_urls,
}

for filepath, content in files.items():
    full_path = os.path.join(BASE_DIR, filepath)
    with open(full_path, 'w') as f:
        f.write(content)
    print(f"Wrote {full_path}")
