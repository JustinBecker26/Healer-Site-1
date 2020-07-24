from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('characters', views.characters, name='characters'),
    path('timeline', views.timeline, name='timeline'),
    path('test', views.test, name='test'),
]
