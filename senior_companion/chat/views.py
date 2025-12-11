from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_room(request, other_user_id):
    # Find the other user
    other_user = get_object_or_404(User, id=other_user_id)
    
    # Get the two user IDs
    user_1_id = request.user.id
    user_2_id = other_user.id
    
    # Sort them to create the consistent room name
    if user_1_id > user_2_id:
        # Swap them
        user_1_id, user_2_id = user_2_id, user_1_id

    # We pass the sorted IDs and the other user's email to the template
    context = {
        'other_user_email': other_user.email,
        'user_1_id': user_1_id,
        'user_2_id': user_2_id,
    }
    return render(request, 'chat/chat_room.html', context)