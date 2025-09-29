from django import forms
from .models import Exercice

class ExerciceForm(forms.ModelForm):
    """Formulaire pour créer un exercice"""

    class Meta:
        model = Exercice
        fields = [
            "nom",
            "groupe_musculaire",
            "series_sugg",
            "reps_sugg",
            "description",
            "image",
        ]
