from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# --- 1. IMPORT our 'resources' views ---
# We need this to link to our public-facing pages
from resources import views as resource_views
from django.views.generic import TemplateView 

urlpatterns = [
    # 1. Main Admin (no change)
    path('admin/', admin.site.urls),

    # 2. Staff Dashboard URLs (we can give this a 'namespace')
    path('dashboard/', include('resources.urls', namespace='staff')),

    # 3. Account URLs (no change)
    path('accounts/', include('users.urls')),
    
    # --- 4. PUBLIC-FACING URLs ---
    # This is the new, cleaner way to add our public pages.
    
    # / (Home Page)
    path('', resource_views.home, name='home'),
    
    # /places/
    path('places/', resource_views.place_list, name='place_list'),

    # --- ADD THIS NEW LINE ---
    # /places/5/ (This is the URL for a specific place, e.g., place #5)
    path('places/<int:place_id>/', resource_views.place_detail, name='place_detail'),
    # --- END OF NEW LINE ---
    
    # /learning/
    path('learning/', resource_views.learning_list, name='learning_list'),
    
    # /hospitals/
    path('hospitals/', resource_views.hospital_list, name='hospital_list'),

    # /hospitals/5/
    path('hospitals/<int:hospital_id>/', resource_views.hospital_detail, name='hospital_detail'),
    

     # --- ADD THIS NEW LINE ---
    path('doctors/<int:doctor_id>/', resource_views.doctor_detail, name='doctor_detail'),
    

     # --- ADD THIS NEW LINE FOR THE GAME VIEW ---
    # Since memory.html is in the root templates folder, this works.
    path('games/memory/', TemplateView.as_view(template_name='memory.html'), name='memory_game'),
    
    
    # /insurance/
    # path('insurance/', resource_views.insurance_list, name='insurance_list'),
    path('insurance/', resource_views.insurance_hub, name='insurance_hub'),


    path('insurance/suggest/', resource_views.insurance_recommendation, name='insurance_recommendation'),
   

     # --- ADD THIS NEW LINE ---
    path('insurance/delete/<int:policy_id>/', resource_views.delete_user_policy, name='delete_user_policy'),
    
    # --- ADD THIS NEW LINE ---
    path('learning/status/<int:resource_id>/', resource_views.update_learning_status, name='update_learning_status'),
    
    # --- ADD THIS NEW LINE ---chats
    path('chat/', include('chat.urls')),

    # --- ADD THIS NEW LINE ---reminders
    path('reminders/', include('reminders.urls')),

    # --- ADD THIS MISSING LINE (This fixes the error) ---
    path('games/', resource_views.game_list, name='game_list'),

    # ... inside urlpatterns ...
    path('games/record/', resource_views.record_game_session, name='record_game_session'),
    
    # --- ADD THIS LINE ---
    path('bot/', include('chatbot.urls')),
    # --- END ADD ---

    # --- ADD THIS NEW LINE FOR CHESS ---
    path('games/chess/', TemplateView.as_view(template_name='chess.html'), name='chess_game'),
    
   
]

if settings.DEBUG:
        
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)