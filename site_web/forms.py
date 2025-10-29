from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import inlineformset_factory
from .models import User, Sexe, Exercice, Entrainement, ExerciceEntrainement, Badge


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'autocomplete': 'off'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )
    last_name = forms.CharField(
        max_length=150,
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )
    email = forms.EmailField(
        label="Courriel",
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3'})
    )
    avatar = forms.ImageField(
        label="Avatar (optionnel)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3'})
    )
    date_naissance = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control mb-3'
        },
        format="%Y-%m-%d"
        )
    )
    sexe = forms.ChoiceField(
        label="Sexe",
        choices=[('', 'Choisir sexe')] + list(Sexe.choices),
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
    )
    taille = forms.DecimalField(
        label="Taille (m)",
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'step': '0.1'})
    )

    poids = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        label="Poids (kg)",
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'step': '0.1'})
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-3',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'})
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
            'class': 'form-control mb-3',
        })
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'})
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
            "nom": forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Nom de l'exercice"}),
            "groupe_musculaire": forms.Select(attrs={"class": "form-select mb-3"}),
            "series_sugg": forms.NumberInput(attrs={"class": "form-control mb-3", "min": 1}),
            "reps_sugg": forms.NumberInput(attrs={"class": "form-control mb-3", "min": 1}),
            "description": forms.Textarea(attrs={"class": "form-control mb-3", "rows": 3, "placeholder": "Ajouter certaines détails sur l'exercice (mouvements, posture, etc.) 20 caractères minimum. 200 caractères maximum."}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control mb-3"}),
        }

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'email', 'date_naissance', 'sexe', 'taille', 'poids')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}),
            'sexe': forms.Select(attrs={'class': 'form-control mb-3'}),
            'taille': forms.NumberInput(attrs={'class': 'form-control mb-3', 'step': '0.1'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control mb-3', 'step': '0.1'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control mb-3'})
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


class EntrainementForm(forms.ModelForm):
    """Formulaire pour créer un entraînement"""

    class Meta:
        model = Entrainement
        fields = [
            "nom",
        ]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Nom de l'entraînement"}),
        }

    exercice_1 = forms.ModelChoiceField(
        queryset=Exercice.objects.filter(est_approuve=True),
        label="Exercice 1",
        widget=forms.Select(attrs={"class": "form-select mb-3"}),
        required=True
    )
    sets_1 = forms.IntegerField(
        label="Séries",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )
    reps_1 = forms.IntegerField(
        label="Répétitions",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )

    exercice_2 = forms.ModelChoiceField(
        queryset=Exercice.objects.filter(est_approuve=True),
        label="Exercice 2",
        widget=forms.Select(attrs={"class": "form-select mb-3"}),
        required=True
    )
    sets_2 = forms.IntegerField(
        label="Séries",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )
    reps_2 = forms.IntegerField(
        label="Répétitions",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )

    exercice_3 = forms.ModelChoiceField(
        queryset=Exercice.objects.filter(est_approuve=True),
        label="Exercice 3",
        widget=forms.Select(attrs={"class": "form-select mb-3"}),
        required=True
    )
    sets_3 = forms.IntegerField(
        label="Séries",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )
    reps_3 = forms.IntegerField(
        label="Répétitions",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )

    exercice_4 = forms.ModelChoiceField(
        queryset=Exercice.objects.filter(est_approuve=True),
        label="Exercice 4",
        widget=forms.Select(attrs={"class": "form-select mb-3"}),
        required=True
    )
    sets_4 = forms.IntegerField(
        label="Séries",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )
    reps_4 = forms.IntegerField(
        label="Répétitions",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "0", "min": 1}),
        required=True
    )


class UserSearchForm(forms.Form):
    """Formulaire de recherche d'utilisateurs"""

    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control w-25 me-3",
            "placeholder": "Rechercher un utilisateur..."
        })
    )


class BadgeForm(forms.ModelForm):
    """Formulaire de création d'un Badge pour les administrateurs du site."""

    class Meta:
        model = Badge
        fields = ["nom", "description", "icone", "categorie", "code"]
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "Nom du badge",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control mb-3",
                "rows": 4,
                "placeholder": "Décrire comment obtenir ce badge.",
            }),
            "categorie": forms.Select(attrs={
                "class": "form-select mb-3",
            }),
            "icone": forms.ClearableFileInput(attrs={
                "class": "form-control mb-3",
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "Laisse vide pour générer automatiquement",
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].required = False

    def clean_code(self):
        code = self.cleaned_data.get("code", "").strip()
        nom = self.cleaned_data.get("nom", "").strip()

        if not code:
            code = slugify(nom)

        code = slugify(code)

        if not code:
            raise forms.ValidationError(
                "Le code (slug) ne peut pas être vide. Veuillez entrer un nom valide."
            )

        return code