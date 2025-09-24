from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Sexe
from django.core.exceptions import ValidationError
from django.utils import timezone


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
            "avatar"
        )

    def clean_title(self):
        """Validation personnalisée du champ title."""
        data = self.cleaned_data['date_naissance']
        if self.date_naissance and self.date_naissance >= timezone.now().date():
            raise ValidationError('La date de début doit être dans le futur')
        return data
