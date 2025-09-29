from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercices/creer/', views.creer_exercice, name='creer_exercice'),
    path('exercices/', views.liste_exercices, name='liste_exercices'),
]