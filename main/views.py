from django.shortcuts import render

def home(request):
    """Home page view - landing page for the social app"""
    return render(request, 'home.html')

def dashboard(request):
    """Dashboard view - main dashboard page"""
    return render(request, 'home.html')