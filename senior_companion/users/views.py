from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # --- 1. ADD THIS IMPORT ---
from .forms import CustomUserCreationForm
from .models import CustomUser
# --- 2. ADD ProfileUpdateForm ---
from .forms import CustomUserCreationForm, ProfileUpdateForm

# This view is correct, no changes needed
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # We don't log them in automatically
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# --- 3. ADD THIS NEW VIEW ---
@login_required # This view is for logged-in users only
def profile(request):
    # Get the profile object linked to the currently logged-in user
    profile = request.user.profile
    
    if request.method == 'POST':
        # If the form is submitted, populate it with the POST data
        # and the existing profile instance
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save() # Save the changes to the profile
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') # Redirect back to the profile page
    else:
        # If it's a GET request, just show the form
        # pre-filled with the user's current profile data
        form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'users/profile.html', {
        'form': form
    })

# --- Companion/Social Views ---

@login_required
def companion_list(request):
    """
    This page shows all other seniors (non-staff)
    and lets the current user add or remove them as companions.
    """
    
    # Get the current user's profile and list of companions
    current_profile = request.user.profile
    my_companions = current_profile.companions.all()
    
    # Get all other senior citizens (non-staff)
    # We must exclude the current user from this list!
    all_other_seniors = CustomUser.objects.filter(
        is_staff=False
    ).exclude(
        pk=request.user.pk
    )

    context = {
        'all_other_seniors': all_other_seniors,
        'my_companions': my_companions,
    }
    return render(request, 'users/companion_list.html', context)

@login_required
def add_companion(request, user_id):
    """
    Finds a user by their ID and adds them to the
    current user's companion list.
    """
    try:
        # Find the user we want to add
        user_to_add = CustomUser.objects.get(pk=user_id)
        
        # Add them to the current user's companion list
        request.user.profile.companions.add(user_to_add)
        
        messages.success(request, f'You have added {user_to_add.email} as a companion.')
    
    except CustomUser.DoesNotExist:
        messages.error(request, 'That user does not exist.')
    
    return redirect('companion_list') # Redirect back to the list

@login_required
def remove_companion(request, user_id):
    """
    Finds a user by their ID and removes them from the
    current user's companion list.
    """
    try:
        # Find the user we want to remove
        user_to_remove = CustomUser.objects.get(pk=user_id)
        
        # Remove them from the current user's companion list
        request.user.profile.companions.remove(user_to_remove)
        
        messages.success(request, f'You have removed {user_to_remove.email} from your companions.')
    
    except CustomUser.DoesNotExist:
        messages.error(request, 'That user does not exist.')
        
    return redirect('companion_list') # Redirect back to the list