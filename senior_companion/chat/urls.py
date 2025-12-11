from django.urls import path
from . import views

urlpatterns = [
    # This URL will be /chat/5/ (to chat with user ID 5)
    path('<int:other_user_id>/', views.chat_room, name='chat_room'),
]