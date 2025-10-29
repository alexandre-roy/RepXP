"""Affichage de la base de données sur la partie admin du site"""

from django.contrib import admin
from .models import User, GroupeMusculaire, Exercice, Entrainement, ExerciceEntrainement, Badge

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Affichage des utilisateurs"""

    list_display = (
        "id",
        "avatar",
        "username",
        "email",
        "first_name",
        "last_name",
        "taille",
        "poids",
        "sexe",
        "date_naissance",
        "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
    )
    list_filter = "sexe", "last_login", "is_superuser", "is_staff", "is_active", "date_joined"
    search_fields = "username", "email", "first_name", "last_name"

@admin.register(GroupeMusculaire)
class GroupeMusculaireAdmin(admin.ModelAdmin):
    """Affichage des groupes musculaires"""

    list_display = (
        "id",
        "nom",
    )
    search_field = "nom"

@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    """Affichage des exercices"""

    list_display = (
        "id",
        "nom",
        "groupe_musculaire",
        "series_sugg",
        "reps_sugg",
        "description",
        "image",
        "est_approuve"
    )
    list_filter = "groupe_musculaire", "series_sugg", "reps_sugg", "est_approuve"
    search_field = "nom"

@admin.register(Entrainement)
class EntrainementAdmin(admin.ModelAdmin):
    """Affichage des entrainements"""

    list_display = (
        "id",
        "nom",
        "date_creation",
        "createur"
    )
    list_filter = "date_creation", "exercices", "createur"
    search_fields = "nom", "exercices", "createur"

@admin.register(ExerciceEntrainement)
class ExerciceEntrainementAdmin(admin.ModelAdmin):
    """Affichage des exercices et entrainements"""

    list_display = (
        "id",
        "entrainement",
        "exercice",
        "sets",
        "reps"
    )
    list_filter = "entrainement", "exercice"
    search_fields = "entrainement", "exercice"


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "categorie",
        "code",
        "description"
    )
    list_filter = ("categorie",)
    search_fields = ("nom", "description")
    prepopulated_fields = {"code": ("nom",)}