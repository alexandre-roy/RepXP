from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import inlineformset_factory
from .models import User, Sexe, Exercice, Entrainement, ExerciceEntrainement


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Courriel",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    avatar = forms.ImageField(
        label="Avatar (optionnel)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    date_naissance = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        },
        format="%Y-%m-%d"
        )
    )
    sexe = forms.ChoiceField(
        label="Sexe",
        choices=[('', 'Choisir sexe')] + list(Sexe.choices),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    taille = forms.DecimalField(
        label="Taille (m)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

    poids = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        label="Poids (kg)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "date_naissance",
            "sexe",
            "taille",
            "poids",
            "password1",
            "password2",
        )

    def clean_title(self):
        """Validation personnalisée du champ title."""
        data = self.cleaned_data['date_naissance']
        if self.date_naissance and self.date_naissance >= timezone.now().date():
            raise ValidationError('La date de début doit être dans le futur')
        return data


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-3',
        })
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control mt-3'})
    )


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
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom de l'exercice"}),
            "groupe_musculaire": forms.Select(attrs={"class": "form-select"}),
            "series_sugg": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "reps_sugg": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Ajouter certaines détails sur l'exercice (mouvements, posture, etc.) 20 caractères minimum. 200 caractères maximum."}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'email', 'date_naissance', 'sexe', 'taille', 'poids')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'taille': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_taille(self):
        taille = self.cleaned_data.get('taille')
        if taille is not None and taille <= 0:
            raise ValidationError("La taille doit être supérieure à 0.")
        return taille

    def clean_poids(self):
        poids = self.cleaned_data.get('poids')
        if poids is not None and poids <= 0:
            raise ValidationError("Le poids doit être supérieur à 0.")
        return poids