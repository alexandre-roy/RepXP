from django.shortcuts import render

# Create your views here.
def index(request):
    """Page d'accueil de activities"""
    return render(request, "mysite/index.html")
