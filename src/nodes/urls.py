from django.urls import path
from . import views

urlpatterns = [
    path('csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('change_chat_title/<int:chat_id>/', views.change_chat_title, name='change_chat_title'),
    path('get_user_chats/', views.get_user_chats, name='get_user_chats'),
    path('get_chat_details/<int:chat_id>/', views.get_chat_details, name='get_chat_details'),
    path('get_response/', views.get_response, name='get_response'),
]