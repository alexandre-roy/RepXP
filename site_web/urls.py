from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('exercices/creer/', views.creer_exercice, name='creer_exercice'),
    path('exercices/', views.liste_exercices, name='liste_exercices'),
    path('signup/', views.register, name='signup'),
    path('accounts/signin', views.connexion, name='signin'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)