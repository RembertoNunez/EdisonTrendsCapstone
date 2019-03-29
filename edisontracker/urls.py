from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tracker-edisontracker'),
    path('map', views.mapGenerate, name='tracker-edisontracker'),


]
