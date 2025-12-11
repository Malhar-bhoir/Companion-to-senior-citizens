from django.urls import path
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # Import our views

urlpatterns = [
    # /accounts/login/
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # /accounts/logout/
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    # /accounts/register/
    path('register/', views.register, name='register'),
    
    # --- ADD THIS NEW LINE ---
    # This creates the URL with name='profile'
    # /accounts/profile/
    path('profile/', views.profile, name='profile'),

    # --- ADD THESE THREE NEW PATHS BELOW ---
    
    # /accounts/companions/
    path('companions/', views.companion_list, name='companion_list'),
    
    # /accounts/companions/add/5/ (example)
    path('companions/add/<int:user_id>/', views.add_companion, name='add_companion'),
    
    # /accounts/companions/remove/5/ (example)
    path('companions/remove/<int:user_id>/', views.remove_companion, name='remove_companion'),
]
