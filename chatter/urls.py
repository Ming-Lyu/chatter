# chat/urls.py
from django.urls import path, re_path
from . import views

app_name = 'chatter'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'room/(?:(?P<room_pk>[0-9]+)/)?$', views.room, name='room'),
]