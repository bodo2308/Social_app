from django.urls import path
from . import views

app_name = 'directory'

urlpatterns = [
    path('', views.directory, name='directory'),
    path('member/<int:user_id>/', views.member_detail, name='member_detail'),
    path('friends/', views.my_friends, name='my_friends'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('respond-friend-request/<int:request_id>/<str:action>/', views.respond_friend_request, name='respond_friend_request'),
    path('cancel-friend-request/<int:request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('remove-friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
]
