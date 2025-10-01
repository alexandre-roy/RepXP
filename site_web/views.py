from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
def review(request):
    if not est_admin(request.user):
        messages.add_message(request, messages.ERROR, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect("index")

    to_review = Exercice.objects.filter(est_approuve=False).count()
    exercice = Exercice.objects.filter(est_approuve=False).first()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "ACCEPTER":
            form = ExerciceForm(request.POST, request.FILES, instance=exercice)
            if form.is_valid():
                approved_exercice = form.save(commit=False)
                approved_exercice.est_approuve = True
                approved_exercice.save()
                messages.add_message(request, messages.INFO, "Exercice accepté !")
                return redirect("review")
        elif action == "REFUSER":
            exercice.delete()
            messages.add_message(request, messages.INFO, "Exercice refusé!")
            return redirect("review")
    else:
        form = ExerciceForm(instance=exercice)

    return render(request, "site_web/exercices/review.html", {
        "form": form,
        "exercices": exercice,
        "to_review": to_review,
        "est_admin": est_admin(request.user)
    })

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
def creer_exercice(request):
    """Vue pour créer un exercice par un admin"""
    if not est_admin(request.user):
        messages.add_message(request, messages.ERROR, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect("index")

    if request.method == "POST":
        form = ExerciceForm(request.POST, request.FILES)
        if form.is_valid():
            approved_exercice = form.save(commit=False)
            approved_exercice.est_approuve = True
            approved_exercice.save()
            messages.success(request, "L'exercice a été créé avec succès")
            return redirect("bank")
    else:
        form = ExerciceForm()

    return render(request, "site_web/exercices/creer_exercice.html", {"form": form, "est_admin": est_admin(request.user)})


@login_required
def proposer_exercice(request):
    """Vue pour proposer un exercice par un utilisateur"""

    if est_admin(request.user):
        return redirect("creer_exercice")

    if request.method == "POST":
        form = ExerciceForm(request.POST, request.FILES)
        if form.is_valid():
            exercice = form.save(commit=False)
            exercice.est_approuve = False
            exercice.save()
            messages.success(request, "Votre exercice a été proposé et est en attente de validation par un administrateur.")
            return redirect("bank")
    else:
        form = ExerciceForm()

    return render(request, "site_web/exercices/proposer_exercice.html", {"form": form, "est_admin": est_admin(request.user)})