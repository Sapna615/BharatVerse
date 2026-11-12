from django.urls import path
from . import views

urlpatterns = [
    # Contributor
    path('', views.contribute, name='contribute'),
    path('success/<int:sub_id>/', views.submission_success, name='submission_success'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('submissions/<int:sub_id>/', views.submission_detail, name='submission_detail'),
    
    # Curator
    path('curator/', views.curator_dashboard, name='curator_dashboard'),
    path('curator/submissions/<int:sub_id>/', views.curator_review, name='curator_review'),
]
