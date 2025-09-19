from django.shortcuts import render

def friends(request):
    """Friends page view - manage connections"""
    return render(request, 'accounts/friends.html')
