from django.shortcuts import render

def inbox(request):
    """Messages inbox view"""
    return render(request, 'messaging/inbox.html')

def newsfeed(request):
    """Newsfeed view"""
    return render(request, 'messaging/newsfeed.html')
