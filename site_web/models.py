"""Modèles pour la base de données"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

# Create your models here.
class Sexe(models.TextChoices):
    """Modèle des sexes"""
    MASCULIN = "M", "Masculin"
    FEMININ = "F", "Féminin"


class User(AbstractUser):
    """Modèle des utilisateurs"""

    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        default='avatars/default_avatar.png'
    )

    date_naissance = models.DateField(
        verbose_name="Date de naissance",
        null=True,
        blank=True,
    )

    sexe = models.CharField(
        max_length=1,
        choices=Sexe.choices,
        default=Sexe.MASCULIN,
        null=True,
        blank=True,
    )

    taille = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taille de l'utilisateur"
    )

    poids = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Poids de l'utilisateur"
    )

    class Meta:
        """Classe meta des utilisateurs"""
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["id"]

    def __str__(self):
        return f"{self.username}"

    def clean(self):
        if self.date_naissance:
            today = timezone.now().date()
            min_birthdate = today - relativedelta(years=15)

            if self.date_naissance > min_birthdate:
                raise ValidationError({
                    'date_naissance': 'Vous devez avoir au moins 15 ans pour vous inscrire.'
                })

        if self.poids:
            if self.poids <= 0:
                raise ValidationError({'poids': "Le poids doit être supérieure à 0."})

        if self.taille:
            if self.taille <= 0:
                raise ValidationError({'taille': "La taille doit être supérieure à 0."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class GroupeMusculaire(models.Model):
    """Modèle des groupes musculaires"""

    nom = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="Nom du groupe musculaire",
        unique=True,
    )

    class Meta:
        """Classe meta des groupes musculaires"""
        verbose_name = "Groupe musculaire"
        verbose_name_plural = "Groupes musculaires"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom}"


class Exercice(models.Model):
    """Modèle des exercices"""

    nom = models.CharField(
        max_length=100,
        blank=False,
        verbose_name="Nom de l'exercice",
        unique=True,
    )

    groupe_musculaire = models.ForeignKey(
        GroupeMusculaire,
        on_delete=models.SET_NULL,
        related_name="exercices",
        verbose_name="Groupe musculaire",
        null=True,
    )

    series_sugg = models.IntegerField(
        blank=False,
        verbose_name="Séries recommandées"
    )

    reps_sugg = models.IntegerField(
        blank=False,
        verbose_name="Répétitions recommandées"
    )

    description = models.CharField(
        max_length=400,
        blank=False,
        verbose_name="Description",
        validators=[MinLengthValidator(20), MaxLengthValidator(400)]
    )

    image = models.ImageField(
        upload_to="images_exercices/",
        blank=True
    )

    est_approuve = models.BooleanField(default=False)

    class Meta:
        """Classe meta des exercices"""
        verbose_name = "Exercice"
        verbose_name_plural = "Exercices"
        ordering = ["nom", "groupe_musculaire"]

    def __str__(self):
        return f"{self.nom}"


class Entrainement(models.Model):
    """Modèle des entrainements"""

    nom = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="Nom de l'entrainement",
    )

    date_creation = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de création"
    )


    exercices = models.ManyToManyField(
        Exercice,
        through="ExerciceEntrainement",
        verbose_name="Exercices",
        blank=True,
    )

    createur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="proposed_exercices",
        verbose_name="Créateur",
        blank=True,
        default="",
        null=False
    )

    class Meta:
        """Classe meta des entrainements"""
        verbose_name = "Entrainement"
        verbose_name_plural = "Entrainements"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom}"


class ExerciceEntrainement(models.Model):
    """Modèle des exercices et entrainements"""
    entrainement = models.ForeignKey(
        Entrainement,
        on_delete=models.CASCADE
    )

    exercice = models.ForeignKey(
        Exercice,
        on_delete=models.CASCADE
    )

    sets = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Sets personnalisés"
    )

    reps = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Répétitions personnalisées"
    )

    class Meta:
        """Classe meta des exercices et entrainements"""
        verbose_name = "Exercice dans l'entraînement"
        verbose_name_plural = "Exercices dans les entraînements"
        ordering = ['entrainement', 'exercice']
        unique_together = ('entrainement', 'exercice')

    def __str__(self):
        return f"{self.exercice} dans {self.entrainement}"




class Badge(models.Model):
    """Modèle des badges"""

    CATEGORIES = [
        ('FORCE', 'Force'),
        ('ENDURANCE', 'Endurance'),
        ('ASSIDUITE', 'Assiduité'),
        ('TECHNIQUE', 'Technique'),
        ('NUTRITION', 'Nutrition'),
        ('AUTRE', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    icone = models.ImageField(upload_to='badges/icones/')
    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    code = models.SlugField(
        unique=True,
        error_messages={
            'unique': "Un badge avec ce code existe déjà. Choississez un autre nom ou laissez le champ vide pour générer automatiquement le code.",
        }
    )

    class Meta:
        ordering = ['nom']
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

    def __str__(self):
        return self.nom
