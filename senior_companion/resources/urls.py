from django.urls import path
from . import views

# This file is ONLY for the staff dashboard, which is
# included at the /dashboard/ path in our main urls.py
app_name = 'resources_staff' # Add an app name for clarity

urlpatterns = [
    # /dashboard/
    path('', views.dashboard_home, name='dashboard_home'),

    # --- ADD THIS NEW LINE ---
    path('places/', views.manage_place_list, name='manage_place_list'),
    
    # /dashboard/places/add/
    path('places/add/', views.add_place, name='add_place'),
    
    # /dashboard/learning/add/
    path('learning/add/', views.add_learning, name='add_learning'),
    
    # /dashboard/hospitals/add/
    path('hospitals/add/', views.add_hospital, name='add_hospital'),
    # --- ADD THESE NEW LINES ---
    path('hospitals/', views.manage_hospitals, name='manage_hospitals'),
    path('doctors/', views.manage_doctors, name='manage_doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    
    # /dashboard/insurance/add/
    path('insurance/add/', views.add_insurance, name='add_insurance'),

    # --- THIS IS THE NEW LINE ---
    # /dashboard/events/add/
    path('events/add/', views.add_event, name='add_event'),

    # /dashboard/places/delete/5/
    path('places/delete/<int:place_id>/', views.delete_place, name='delete_place'),



    path('games/', views.manage_games, name='manage_games'),
    path('games/add/', views.add_game, name='add_game'),
]