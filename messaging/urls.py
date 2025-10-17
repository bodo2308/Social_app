from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
]
