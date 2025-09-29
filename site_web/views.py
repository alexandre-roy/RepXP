from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import ExerciceForm
from .models import Exercice

# Create your views here.
def index(request):
    """Page d'accueil de activities"""
    return render(request, "site_web/index.html")

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

    return render(request, "exercices/creer_exercice.html", {"form": form})


def liste_exercices(request):
    """Vue pour afficher la liste des exercices"""
    exercices = Exercice.objects.all()
    return render(request, "exercices/liste_exercices.html", {"exercices": exercices})