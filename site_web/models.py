from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
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
        blank=True
    )

    date_naissance = models.DateField(
        verbose_name="Date de naissance",
        blank=False
    )

    sexe = models.CharField(
        max_length=1,
        choices=Sexe.choices,
        default=Sexe.MASCULIN
    )

    taille = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=False,
        verbose_name="Taille de l'utilisateur"
    )

    poids = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=False,
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

    series = models.IntegerField(
        blank=False,
        verbose_name="Séries recommandées"
    )

    reps = models.IntegerField(
        blank=False,
        verbose_name="Répétitions recommandées"
    )

    description = models.CharField(
        max_length=400,
        blank=False,
        verbose_name="Description",
        validators=[MinLengthValidator(20)],
    )

    image = models.ImageField(
        upload_to="images_exercices/",
        blank=True
    )

    class Meta:
        """Classe meta des exercices"""
        verbose_name = "Exercice"
        verbose_name_plural = "Exercices"
        ordering = ["groupe_musculaire", "nom"]

    def __str__(self):
        return f"{self.nom}"


# class Entrainement(models.Model):
#     """Modèle des entrainements"""
#
#     nom = models.CharField(
#         max_length=50,
#         blank=False,
#         verbose_name="Nom de l'entrainement",
#     )
#
#     exercice_1 = models.ForeignKey(
#         Exercice,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name="Exercice principal"
#     )
