from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from .forms import ExerciceForm, RegisterForm, ConnexionForm
from .models import Exercice 

# Create your views here.
def est_admin(user):
    return user.is_authenticated and user.is_staff

def index(request):
    """Page d'accueil de activities"""
    return render(request, "site_web/index.html", {"est_admin": est_admin(request.user)})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Compte créé avec succès!")
            return redirect('signin')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form, "est_admin": est_admin(request.user)})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = ConnexionForm(request)

    return render(request, 'registration/login.html', {'form': form, "est_admin": est_admin(request.user)})

@login_required
@user_passes_test(est_admin)
def review(request):
    to_review = Exercice.objects.filter(est_approuve = False).count()
    exercice = Exercice.objects.filter(est_approuve = False).first()
    action = request.POST.get("action")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "ACCEPTER":
            form = ExerciceForm(request.POST, request.FILES, instance=exercice)
            if form.is_valid():
                approved_exercice = form.save(commit=False)
                approved_exercice.est_approuve = True
                approved_exercice.save()
                messages.add_message(request, messages.INFO, "Exercice accepté !")
        elif action == "REFUSER":
            exercice.delete()
            messages.add_message(request, messages.INFO, "Exercice refusé!")
        return redirect("review")

    else:
        form = ExerciceForm(instance=exercice)

    return render(request, 'site_web/exercices/review.html',
                  {'exercices': exercice, "est_admin": est_admin(request.user), "form": form, "to_review": to_review})

@login_required
def bank(request):
    recherche = request.GET.get("recherche")
    exercices = Exercice.objects.filter(est_approuve=True)

    if recherche:
        exercices = exercices.filter(nom__icontains=recherche)
    return render(request, 'site_web/exercices/bank.html', {
        'exercices': exercices,
        'est_admin': est_admin(request.user)
    })

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

    return render(request, "site_web/exercices/creer_exercice.html", {"form": form, "est_admin": est_admin(request.user)})

def liste_exercices(request):
    """Vue pour afficher la liste des exercices"""
    exercices = Exercice.objects.all()
    return render(request, "site_web/exercices/liste_exercices.html", {"exercices": exercices, "est_admin": est_admin(request.user)})