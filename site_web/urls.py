from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercices/new/', views.creer_exercice, name='creer_exercice'),
    path('exercices/review', views.review, name='review'),
    path('exercices/bank', views.bank, name='bank'),
    path('exercices/proposer', views.proposer_exercice, name='proposer_exercice'),
    path('workouts/new', views.new_workout, name='new_workout'),
    path('workouts/', views.my_workouts, name='my_workouts'),
    path('signup/', views.register, name='signup'),
    path('accounts/signin', views.connexion, name='signin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profil/', views.profile, name="profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)