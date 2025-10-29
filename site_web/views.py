from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import ExerciceForm, RegisterForm, ConnexionForm, EntrainementForm, UserSearchForm, CustomUserChangeForm, BadgeForm
from .models import Exercice, ExerciceEntrainement, User, Entrainement, Badge

# Create your views here.
def est_admin(user):
    return user.is_authenticated and user.is_staff

def index(request):
    """Page d'accueil de activities"""
    return render(request, "site_web/index.html", {"est_admin": est_admin(request.user)})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès!")
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
        messages.error(request,  "Vous n'avez pas la permission d'accéder à cette page.")
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
                messages.success(request,  "Exercice accepté !")
                return redirect("review")
        elif action == "REFUSER":
            exercice.delete()
            messages.success(request, "Exercice refusé!")
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
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
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

@login_required
def new_workout(request):
    """Vue pour créer un nouvel entraînement"""
    if request.method == "POST":
        form = EntrainementForm(request.POST)
        if form.is_valid():
            exercices_ids = []
            for i in range(1, 5):
                ex_id = form.cleaned_data[f"exercice_{i}"].id
                if ex_id in exercices_ids:
                    messages.error(request, "Vous ne pouvez pas utiliser le même exercice plusieurs fois.")
                    return render(request, "site_web/workouts/new_workout.html", {"form": form, "est_admin": est_admin(request.user)})
                exercices_ids.append(ex_id)

            entrainement = Entrainement.objects.create(
                nom=form.cleaned_data["nom"],
                createur=request.user
            )

            for i in range(1, 5):
                ExerciceEntrainement.objects.create(
                    entrainement=entrainement,
                    exercice=form.cleaned_data[f"exercice_{i}"],
                    sets=form.cleaned_data[f"sets_{i}"],
                    reps=form.cleaned_data[f"reps_{i}"]
                )

            messages.success(request, "Entraînement créé avec succès!")
            return redirect("my_workouts")
    else:
        form = EntrainementForm()
    return render(request, "site_web/workouts/new_workout.html", {"form": form, "est_admin": est_admin(request.user)})

@login_required
def edit_workout(request, workout_id):
    """Vue pour modifier mes entrainements"""
    entrainement = Entrainement.objects.get(id=workout_id)
    exercices = ExerciceEntrainement.objects.filter(entrainement_id=workout_id)

    if entrainement.createur == request.user:
        if request.method == 'POST':
            form = EntrainementForm(request.POST)
            if form.is_valid():
                exercices_ids = []
                for i in range(1, 5):
                    ex_id = form.cleaned_data[f"exercice_{i}"].id
                    if ex_id in exercices_ids:
                        messages.error(request, "Vous ne pouvez pas utiliser le même exercice plusieurs fois.")
                        return render(request, 'site_web/workouts/edit_workout.html', {"est_admin": est_admin(request.user), "entrainement": entrainement, "form": form, "exercices": exercices})
                    exercices_ids.append(ex_id)

                entrainement.nom = form.cleaned_data["nom"]
                entrainement.save()

                for i, exercice in enumerate(exercices, 1):
                    exercice.exercice = form.cleaned_data[f"exercice_{i}"]
                    exercice.sets = form.cleaned_data[f"sets_{i}"]
                    exercice.reps = form.cleaned_data[f"reps_{i}"]
                    exercice.save()

                messages.success(request, "Entraînement modifié !")
                return redirect("my_workouts")
        else:
            initial_data = {"nom": entrainement.nom}

            for i, exercice in enumerate(exercices, start=1):
                initial_data[f"exercice_{i}"] = exercice.exercice
                initial_data[f"sets_{i}"] = exercice.sets
                initial_data[f"reps_{i}"] = exercice.reps

            form = EntrainementForm(initial=initial_data)
    else:
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect("index")

    return render(request, 'site_web/workouts/edit_workout.html', {"est_admin": est_admin(request.user), "entrainement": entrainement, "form": form, "exercices": exercices})

@login_required
def my_workouts(request):
    """Vue pour voir mes entraînements"""
    recherche = request.GET.get("recherche")
    entrainements = Entrainement.objects.filter(createur=request.user).prefetch_related('exerciceentrainement_set')

    if recherche:
        entrainements = entrainements.filter(nom__icontains=recherche)
    return render(request, 'site_web/workouts/my_workouts.html', {
        "entrainements": entrainements, "est_admin": est_admin(request.user)})

@login_required
def profile(request):
    return render(
        request,
        "site_web/profil/profil.html",
        {"user": request.user, "est_admin": est_admin(request.user)}
    )

@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil modifié avec succès!")

            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'site_web/profil/edit_profil.html', {'form': form, "est_admin": est_admin(request.user)})

@login_required
def user_search(request):
    """Vue pour rechercher des utilisateurs"""

    form = UserSearchForm(request.GET or None)
    if request.user.is_staff or request.user.is_superuser:
        users = User.objects.all().order_by("username")
    else:
        users = User.objects.filter(is_staff=False, is_superuser=False).order_by("username")

    if form.is_valid():
        username = form.cleaned_data.get("username") or ""
        if username:
            users = users.filter(username__icontains=username)

    paginator = Paginator(users, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "site_web/users/search.html",
        {
            "form": form,
            "page_obj": page_obj,
            "username": form.cleaned_data.get("username") if form.is_valid() else "", "est_admin": est_admin(request.user)
        },
    )

@login_required
def delete_workout(request, workout_id):
    """Vue pour supprimer un entraînement"""
    if request.method == "POST":
        entrainement = Entrainement.objects.get(id=workout_id, createur=request.user)
        entrainement.delete()
        messages.success(request, "Entraînement supprimé avec succès!")
    return redirect("my_workouts")


@login_required
def view_other_user_profile(request, user_id):
    """Vue pour voir le profil d'un autre utilisateur"""
    user = get_object_or_404(get_user_model(), id=user_id)

    if not request.user.is_staff and not request.user.is_superuser:
        if user.is_staff or user.is_superuser:
            messages.error(request, "Vous n'avez pas la permission de voir ce profil.")
            return redirect("index")

    return render(
        request,
        "site_web/profil/other_user_profile.html",
        {"user": user, "est_admin": est_admin(request.user)}
    )

@login_required
def create_badge(request):
    """Vue permettant à un administrateur de créer un nouveau badge."""

    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect("index")

    if request.method == "POST":
        form = BadgeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Badge créé avec succès !")
            return redirect("badge_list")
    else:
        form = BadgeForm()

    return render(request, "site_web/badges/create_badge.html", {"form": form})

@login_required
def badge_list(request):
    """Vue pour afficher la liste des badges disponibles."""
    badges = Badge.objects.all().order_by("categorie", "nom")
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect("index")
    return render(request, "site_web/badges/badge_list.html", {"badges": badges})