from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .recommendation_form import RecommendationInputForm # <-- Add this
from .ml_service import get_insurance_recommendation # <-- Add this
from django.db import models # <-- ADD THIS IMPORT
from django.http import JsonResponse
from django.utils import timezone
# --- 1. UPDATED IMPORTS ---
# We've added EventForm and the Event model
from .forms import (
    PlaceForm, 
    LearningResourceForm, 
    HospitalForm, 
    InsurancePolicyForm,
    EventForm,
    PlaceImageForm,
    UserPolicyForm,
    DoctorForm , 
    GameForm
    
)
from .models import (
    PlaceToVisit, 
    LearningResource, 
    Hospital, 
    InsurancePolicy,
    Event,
    UserInsurancePolicy,
    Doctor,
    LearningProgress,
    Game
    
)


# --- 2. UPGRADED 'HOME' VIEW ---
# This view is now personalized!
def home(request):
    context = {}
    # We only want to show personalized content to logged-in seniors
    if request.user.is_authenticated and not request.user.is_staff:
        try:
            # Get the user's profile and their selected hobbies
            profile = request.user.profile
            user_hobbies = profile.hobbies.all()
            
            if user_hobbies:
                # Find Events and Learning Resources matching their hobbies
                # We use hobby__in=... to find matches in their list
                # We use order_by('event_date') to show upcoming events first
                # We use [:3] to show only the top 3
                
                personalized_events = Event.objects.filter(
                    hobby__in=user_hobbies
                ).order_by('event_date')[:3]

                personalized_learning = LearningResource.objects.filter(
                    category__in=user_hobbies
                )[:3]

                context['personalized_events'] = personalized_events
                context['personalized_learning'] = personalized_learning
        
        except AttributeError:
            # This handles a rare case where a profile might not exist yet
            pass 
            
    return render(request, 'resources/home.html', context)

# --- Staff Dashboard Views ---

# This decorator is correct and needs no changes
def staff_required(view_func):
    """
    Decorator that checks if a user is logged in AND is a staff member.
    """
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@staff_required
def dashboard_home(request):
    return render(request, 'resources/dashboard_home.html')

@staff_required
def manage_place_list(request):
    """
    Shows a list of all places for staff to manage.
    """
    places = PlaceToVisit.objects.all().order_by('name')
    context = {
        'places': places
    }
    return render(request, 'resources/manage_place_list.html', context)

# @staff_required
# def add_place(request):
#     if request.method == 'POST':
#         form = PlaceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'New Place to Visit added successfully!')
#             # --- FIX 1 ---
#             # Changed 'dashboard_home' to 'staff:dashboard_home'
#             return redirect('staff:dashboard_home')
#     else:
#         form = PlaceForm()
    
#     return render(request, 'resources/resource_form.html', {
#         'form': form,
#         'title': 'Add a New Place to Visit'
#     })

@staff_required
def add_place(request):
    if request.method == 'POST':
        # form = PlaceForm(request.POST)
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Place to Visit added successfully!')
            return redirect('staff:dashboard_home')
    else:
        form = PlaceForm()
    
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': 'Add a New Place to Visit'
    })

# @staff_required
# def add_learning(request):
#     if request.method == 'POST':
#         form = LearningResourceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'New Learning Resource added successfully!')
#             # --- FIX 2 ---
#             # Changed 'dashboard_home' to 'staff:dashboard_home'
#             return redirect('staff:dashboard_home')
#     else:
#         form = LearningResourceForm()
    
#     return render(request, 'resources/resource_form.html', {
#         'form': form,
#         'title': 'Add a New Learning Resource'
#     })

@staff_required
def add_learning(request):
    if request.method == 'POST':
        # --- CRITICAL CHANGE: Added request.FILES ---
        form = LearningResourceForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'New Learning Resource added successfully!')
            return redirect('staff:dashboard_home')
        else:
            messages.error(request, 'There was an error adding your learning resource. Please check the fields below.')
    else:
        form = LearningResourceForm()
    
    # --- CRITICAL CHANGE: Changed template name ---
    return render(request, 'resources/add_learning_form.html', {
        'form': form,
        'title': 'Add a New Learning Resource'
    })

@staff_required
def add_hospital(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Hospital added successfully!')
            # --- FIX 3 ---
            # Changed 'dashboard_home' to 'staff:dashboard_home'
            return redirect('staff:dashboard_home')
    else:
        form = HospitalForm()
    
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': 'Add a New Hospital'
    })

@staff_required
def add_insurance(request):
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Insurance Policy added successfully!')
            # --- FIX 4 ---
            # Changed 'dashboard_home' to 'staff:dashboard_home'
            return redirect('staff:dashboard_home')
    else:
        form = InsurancePolicyForm()
    
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': 'Add a New Insurance Policy'
    })


# --- 3. ADDED 'ADD_EVENT' VIEW ---
@staff_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Don't save yet, we need to add the creator!
            event = form.save(commit=False)
            event.created_by = request.user  # Set the creator to the logged-in staff
            event.save() # Now save the event
            
            messages.success(request, 'New Event added successfully!')
            # --- FIX 5 ---
            # Changed 'dashboard_home' to 'staff:dashboard_home'
            return redirect('staff:dashboard_home')
    else:
        form = EventForm()
    
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': 'Add a New Event'
    })


# --- Public-Facing List Views (No Changes Needed) ---

@login_required
def place_list(request):
    places = PlaceToVisit.objects.all()
    context = {
        'places': places
    }
    return render(request, 'resources/place_list.html', context)

@login_required
def learning_list(request):
    """
    Displays the list of learning resources with advanced filtering and search.
    Also retrieves the current user's progress for each resource.
    """
    resources = LearningResource.objects.all().order_by('title')
    
    # Get parameters
    query = request.GET.get('q')
    content_type_filter = request.GET.get('content_type')
    difficulty_filter = request.GET.get('difficulty')

    # --- SEARCH LOGIC ---
    if query:
        resources = resources.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query)
        )
    
    # --- FILTER LOGIC ---
    if content_type_filter:
        resources = resources.filter(content_type=content_type_filter)
        
    if difficulty_filter:
        resources = resources.filter(difficulty=difficulty_filter)

    # --- PROGRESS TRACKING (CRITICAL) ---
    # Get all progress records for the current user
    user_progress = LearningProgress.objects.filter(user=request.user).values(
        'resource_id', 'status'
    )
    # Convert list of dicts to a dict mapping {resource_id: status} for easy lookup
    progress_map = {item['resource_id']: item['status'] for item in user_progress}

    context = {
        'resources': resources,
        'query': query,
        'content_types': LearningResource.CONTENT_CHOICES, # Choices for filter
        'difficulties': LearningResource.DIFFICULTY_CHOICES, # Choices for filter
        'progress_map': progress_map, # Pass progress data to the template
        'content_type_filter': content_type_filter,
        'difficulty_filter': difficulty_filter,
    }
    return render(request, 'resources/learning_list.html', context)

# @login_required
# def hospital_list(request):
#     """
#     Displays the list of hospitals with search and filter capabilities, 
#     including a nearby emergency filter.
#     """
#     # Start with all hospitals
#     hospitals = Hospital.objects.all()
    
#     # Get parameters
#     query = request.GET.get('q')
#     filter_geriatrics = request.GET.get('filter_geriatrics')
#     filter_wheelchair = request.GET.get('filter_wheelchair')
#     filter_emergency = request.GET.get('filter_emergency') # <-- NEW PARAMETER

#     # --- SEARCH LOGIC (by Name, Specialty, or City/State) ---
#     if query:
#         # Search across name, specialty, city, and state
#         hospitals = hospitals.filter(
#             models.Q(name__icontains=query) |
#             models.Q(specialty__icontains=query) |
#             models.Q(city__icontains=query) | # <-- New search fields
#             models.Q(state__icontains=query) 
#         )
    
#     # --- FILTER LOGIC ---
    
#     # 1. Emergency Filter (triggered by the new button)
#     if filter_emergency == 'on':
#         hospitals = hospitals.filter(is_emergency_24h=True)
#         # Note: The query (q) handles the location filter (e.g., 'q=Mumbai')
        
#     # 2. Geriatrics Filter
#     if filter_geriatrics == 'on':
#         hospitals = hospitals.filter(has_geriatrics_dept=True)
        
#     # 3. Wheelchair Filter
#     if filter_wheelchair == 'on':
#         hospitals = hospitals.filter(is_wheelchair_accessible=True)

#     context = {
#         'hospitals': hospitals,
#         'query': query,
#         'filter_geriatrics': filter_geriatrics,
#         'filter_wheelchair': filter_wheelchair,
#         'filter_emergency': filter_emergency, # Pass back to template if needed
#     }
#     return render(request, 'resources/hospital_list.html', context)

@login_required
def hospital_list(request):
    """
    Displays the list of hospitals with search and filter capabilities,
    prioritizing the user's home location for nearby search.
    """
    hospitals = Hospital.objects.all()
    
    # Get parameters
    query = request.GET.get('q')
    filter_geriatrics = request.GET.get('filter_geriatrics')
    filter_wheelchair = request.GET.get('filter_wheelchair')
    
    # --- NEW: Get User Location for Maps Search ---
    user_city = request.user.profile.home_address_city
    user_state = request.user.profile.home_address_state
    
    # Construct a clean address string for Google Maps
    google_maps_address = f"emergency hospital near {user_city}, {user_state}"
    
    # --- Filter/Search Logic (Rest of the logic remains the same for the main list) ---
    # 1. Nearby Search Trigger (using user's saved location)
    if request.GET.get('nearby_emergency') == 'on':
        if user_city:
            # Set query to user's city and filter to emergency 
            hospitals = hospitals.filter(
                models.Q(city__icontains=user_city) |
                models.Q(state__icontains=user_state),
                is_emergency_24h=True
            ).order_by('city')
            messages.info(request, f"Showing 24/7 Emergency Hospitals near your saved location: {user_city}.")
        else:
            messages.warning(request, "Please save your city/state in 'My Profile' to enable nearby search.")
            hospitals = hospitals.filter(is_emergency_24h=True) # Fallback to show all emergency

    # 2. General Search (by query)
    elif query:
        # Search across name, specialty, city, and state
        hospitals = hospitals.filter(
            models.Q(name__icontains=query) |
            models.Q(specialty__icontains=query) |
            models.Q(city__icontains=query) |
            models.Q(state__icontains=query)
        )
    
    # 3. Geriatrics Filter
    if filter_geriatrics == 'on':
        hospitals = hospitals.filter(has_geriatrics_dept=True)
        
    # 4. Wheelchair Filter
    if filter_wheelchair == 'on':
        hospitals = hospitals.filter(is_wheelchair_accessible=True)

    context = {
        'hospitals': hospitals,
        'query': query,
        'filter_geriatrics': filter_geriatrics,
        'filter_wheelchair': filter_wheelchair,
        
        # --- NEW CONTEXT VARIABLE ---
        'google_maps_address': google_maps_address,
        'user_city': user_city,
        # --- END NEW CONTEXT VARIABLE ---
    }
    return render(request, 'resources/hospital_list.html', context)

@login_required
def insurance_list(request):
    policies = InsurancePolicy.objects.all()
    context = {
        'policies': policies
    }
    return render(request, 'resources/insurance_list.html', context)

# --- PUBLIC-FACING DETAIL VIEW ---

# @login_required
# def place_detail(request, place_id):
#     """
#     Shows a single, detailed page for a PlaceToVisit.
#     This is the "View More" page.
#     """
#     place = get_object_or_404(PlaceToVisit, id=place_id)
    
#     # In the next phase, we will also get the gallery_images here
#     # gallery_images = place.gallery_images.all()
    
#     context = {
#         'place': place,
#     }
#     return render(request, 'resources/place_detail.html', context)

@login_required
def place_detail(request, place_id):
    """
    Shows a single, detailed page for a PlaceToVisit.
    
    - For SENIORS: Shows the place details and gallery.
    - For STAFF: Also shows a form to add new gallery images.
    """
    place = get_object_or_404(PlaceToVisit, id=place_id)
    gallery_images = place.gallery_images.all()
    
    # This is the form for staff to add a new gallery image
    image_form = PlaceImageForm()

    # Handle the "Add Image" form submission (only if user is staff)
    if request.method == 'POST' and request.user.is_staff:
        form = PlaceImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save(commit=False)
            image_upload.place = place # Link the image to this place
            image_upload.save()
            messages.success(request, 'New gallery image added successfully!')
            return redirect('place_detail', place_id=place.id)
        else:
            messages.error(request, 'There was an error uploading your image.')

    context = {
        'place': place,
        'gallery_images': gallery_images,
        'image_form': image_form, # Pass the form to the template
    }
    return render(request, 'resources/place_detail.html', context)

@staff_required
@require_POST  # This view only accepts POST requests (for security)
def delete_place(request, place_id):
    """
    Deletes a PlaceToVisit object.
    """
    # Find the place, but make sure the user is staff
    # (though staff_required already checks this, it's good practice)
    place = get_object_or_404(PlaceToVisit, id=place_id)
    place_name = place.name
    
    place.delete()
    
    messages.success(request, f'The place "{place_name}" was deleted successfully.')
    
    # Redirect back to the staff's "manage list" page
    return redirect('staff:manage_place_list')

@login_required
def insurance_hub(request):
    """
    The main Insurance Hub for seniors.
    Shows 'My Policies' and 'Recommended Policies'.
    Handles adding a new personal policy.
    """
    # 1. Get the user's personal policies
    my_policies = UserInsurancePolicy.objects.filter(user=request.user).order_by('expiry_date')
    
    # 2. Get staff-recommended policies
    recommended_policies = InsurancePolicy.objects.all()
    
    # 3. Handle the "Add Policy" form
    if request.method == 'POST':
        form = UserPolicyForm(request.POST, request.FILES)
        if form.is_valid():
            new_policy = form.save(commit=False)
            new_policy.user = request.user
            new_policy.save()
            messages.success(request, 'Your policy has been added successfully!')
            return redirect('insurance_hub')
    else:
        form = UserPolicyForm()

    context = {
        'my_policies': my_policies,
        'recommended_policies': recommended_policies,
        'form': form
    }
    return render(request, 'resources/insurance_hub.html', context)

@login_required
@require_POST
def delete_user_policy(request, policy_id):
    policy = get_object_or_404(UserInsurancePolicy, id=policy_id, user=request.user)
    policy.delete()
    messages.success(request, 'Policy removed successfully.')
    return redirect('insurance_hub')


@login_required
def insurance_recommendation(request):
    """
    Displays the form to get user data and shows the ML recommendation result.
    """
    recommendation_result = None
    
    if request.method == 'POST':
        form = RecommendationInputForm(request.POST)
        if form.is_valid():
            # Get data as a dictionary of cleaned strings
            user_input = form.cleaned_data 
            
            # Call the ML service
            prediction = get_insurance_recommendation(user_input)
            
            recommended_policies = prediction
            
    else:
        form = RecommendationInputForm()
        # Initialize an empty list if no post yet
        recommended_policies = [] 

    context = {
        'form': form,
        'recommended_policies': recommended_policies, # <-- NEW CONTEXT VARIABLE
        'title': 'Personalized Insurance Suggestion'
    }
    return render(request, 'resources/insurance_recommendation.html', context)

@staff_required
def manage_hospitals(request):
    """Shows a list of all hospitals for staff to manage."""
    hospitals = Hospital.objects.all().order_by('name')
    context = {
        'hospitals': hospitals,
        'title': 'Manage Hospitals',
        'add_url': 'staff:add_hospital',
        'manage_doctors_url': 'staff:manage_doctors',
    }
    return render(request, 'resources/manage_list_generic.html', context)

@staff_required
def manage_doctors(request):
    """Shows a list of all doctors for staff to manage."""
    doctors = Doctor.objects.all().order_by('name')
    context = {
        'doctors': doctors,
        'title': 'Manage Doctors',
        'add_url': 'staff:add_doctor',
    }
    return render(request, 'resources/manage_doctor_list.html', context)

@staff_required
def add_doctor(request):
    if request.method == 'POST':
        # Files are included for the profile photo
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Doctor profile added successfully!')
            return redirect('staff:manage_doctors')
    else:
        form = DoctorForm()
    
    return render(request, 'resources/add_doctor_form.html', {
        'form': form,
        'title': 'Add a New Doctor Profile'
    })

@login_required
def hospital_detail(request, hospital_id):
    """
    Shows details of a single Hospital and lists all affiliated doctors.
    """
    hospital = get_object_or_404(Hospital, id=hospital_id)
    affiliated_doctors = hospital.affiliated_doctors.all().order_by('specialty')
    
    context = {
        'hospital': hospital,
        'affiliated_doctors': affiliated_doctors,
    }
    return render(request, 'resources/hospital_detail.html', context)

@login_required
def doctor_detail(request, doctor_id):
    """
    Shows the detailed profile page for a single Doctor.
    """
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    context = {
        'doctor': doctor,
    }
    return render(request, 'resources/doctor_detail.html', context)


@login_required
@require_POST
def update_learning_status(request, resource_id):
    """
    Updates the status (Bookmarked, Completed, etc.) for a specific resource.
    """
    resource = get_object_or_404(LearningResource, id=resource_id)
    status_key = request.POST.get('status')
    
    if status_key in dict(LearningProgress.STATUS_CHOICES):
        # Use update_or_create to handle both creation and updates safely
        progress, created = LearningProgress.objects.update_or_create(
            user=request.user,
            resource=resource,
            defaults={'status': status_key}
        )
        
        # Determine the user-friendly message
        action = "Bookmarked" if status_key == 'bookmarked' else status_key.replace('_', ' ').capitalize()
        messages.success(request, f'Resource "{resource.title}" status updated to: {action}.')
    else:
        messages.error(request, 'Invalid status action.')

    # Redirect back to the learning list page
    return redirect('learning_list')

@staff_required
def manage_games(request):
    """Shows a list of all games for staff to manage."""
    games = Game.objects.all().order_by('name')
    context = {
        'games': games,
        'title': 'Manage Game Library',
    }
    return render(request, 'resources/manage_games.html', context)

@staff_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'New game "{form.cleaned_data["name"]}" added successfully!')
            return redirect('staff:manage_games')
    else:
        form = GameForm()
    
    return render(request, 'resources/add_game_form.html', {
        'form': form,
        'title': 'Add New Game'
    })

@login_required
def game_list(request):
    """
    Displays the list of games curated for seniors.
    """
    games = Game.objects.all().order_by('name')
    context = {
        'games': games,
    }
    return render(request, 'resources/game_list.html', context)

@login_required
@require_POST
def record_game_session(request):
    """
    AJAX view to save the result of a game.
    """
    game_name = request.POST.get('game_name')
    score = request.POST.get('score')
    outcome = request.POST.get('outcome')
    
    # Find the game object
    # (We use filter().first() to avoid crashes if the name is slightly off)
    game = Game.objects.filter(name__icontains=game_name).first()
    
    if game and score:
        GameSession.objects.create(
            user=request.user,
            game=game,
            score=int(score),
            outcome=outcome,
            end_time=timezone.now()
        )
        return JsonResponse({'status': 'success', 'message': 'Score saved'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid game data'}, status=400)
