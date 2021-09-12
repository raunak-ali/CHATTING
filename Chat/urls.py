# chat/urls.py
from django.urls import path

from . import views
app_name='Chat'
urlpatterns = [
    path('chat/<str:room_name>/', views.room, name='Room'),
]