from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm, ConnexionForm

# Create your views here.
def index(request):
    """Page d'accueil de activities"""
    return render(request, "site_web/index.html")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Compte créé avec succès!")
            return redirect('connexion')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = ConnexionForm(request)
    
    return render(request, 'registration/login.html', {'form': form})

