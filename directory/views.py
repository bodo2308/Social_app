from django.shortcuts import render

def directory(request):
    """Directory page view - member directory"""
    return render(request, 'directory/directory.html')
