from django.urls import path, include
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
