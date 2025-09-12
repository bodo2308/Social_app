from django.urls import path
from . import views

app_name = 'directory'

urlpatterns = [
    # Placeholder URLs - to be implemented
    path('', views.index, name='index'),
]
