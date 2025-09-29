from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from .forms import ExerciceForm, RegisterForm, ConnexionForm
from .models import Exercice

# Create your views here.
def index(request):
    """Page d'accueil de activities"""
    return render(request, "site_web/index.html")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Compte créé avec succès!")
            return redirect('connexion')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def review(request):
    exercices = Exercice.objects.filter(est_approuve = False)
    return render(request, 'site_web/review.html', {'exercices': exercices})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = ConnexionForm(request)

    return render(request, 'registration/login.html', {'form': form})



def est_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(est_admin)
def creer_exercice(request):
    """Vue pour créer un exercice par un admin"""

    if request.method == "POST":
        form = ExerciceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "L'exercice a été créé avec succès ✅")
            return redirect("liste_exercices")
    else:
        form = ExerciceForm()

    return render(request, "site_web/exercices/creer_exercice.html", {"form": form})


def liste_exercices(request):
    """Vue pour afficher la liste des exercices"""
    exercices = Exercice.objects.all()
    return render(request, "site_web/exercices/creer_exercice.html", {"exercices": exercices})