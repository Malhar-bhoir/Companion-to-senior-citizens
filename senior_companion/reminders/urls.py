from django.urls import path
from . import views

urlpatterns = [
    # /reminders/ - The main list and add page
    path('', views.medication_list, name='medication_list'),
    
    # /reminders/add_time/5/ - Add reminder to med #5
    path('add_time/<int:medication_id>/', views.add_reminder, name='add_reminder'),
    
    # /reminders/delete_med/5/ - Delete med #5
    path('delete_med/<int:medication_id>/', views.delete_medication, name='delete_medication'),
    
    # /reminders/delete_time/12/ - Delete reminder #12
    path('delete_time/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
]