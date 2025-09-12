from django.shortcuts import render
from django.http import HttpResponse

def inbox(request):
    return HttpResponse("Messages Inbox - Coming soon!")

def newsfeed(request):
    return HttpResponse("Newsfeed - Coming soon!")
