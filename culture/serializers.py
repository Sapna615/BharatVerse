from rest_framework import serializers
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
