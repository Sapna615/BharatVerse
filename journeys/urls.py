from django.urls import path
from .views import my_journey, toggle_journey_item

urlpatterns = [
    path('', my_journey, name='my_journey'),
    path('toggle/<int:item_id>/', toggle_journey_item, name='toggle_journey_item'),
]
