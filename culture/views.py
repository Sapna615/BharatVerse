from rest_framework import viewsets, permissions
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
