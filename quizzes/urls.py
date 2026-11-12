from django.urls import path
from .views import quiz_list, quiz_detail, take_quiz, quiz_result

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<slug:slug>/', quiz_detail, name='quiz_detail'),
    path('<slug:slug>/take/', take_quiz, name='take_quiz'),
    path('result/<int:attempt_id>/', quiz_result, name='quiz_result'),
]
