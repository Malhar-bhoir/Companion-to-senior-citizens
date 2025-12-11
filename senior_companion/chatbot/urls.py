from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.chat_api, name='chat_api'),
]