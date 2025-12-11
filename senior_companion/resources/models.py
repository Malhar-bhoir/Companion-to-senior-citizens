from django.db import models
from django.utils import timezone
# --- IMPORT OUR HOBBY & USER MODELS ---
# We need these to link to our new models
from users.models import CustomUser, Hobby 
from django.conf import settings # <-- Make sure this is imported
# --- NO CHANGES TO THESE 3 MODELS ---

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=200, blank=True)

    # Accessibility and Emergency Status (Your Suggestions #3)
    is_emergency_24h = models.BooleanField(default=False)
    is_wheelchair_accessible = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_geriatrics_dept = models.BooleanField(default=False, verbose_name="Has Geriatrics Department")


    def __str__(self):
        return self.name

class InsurancePolicy(models.Model):
    POLICY_CHOICES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('home', 'Home Insurance'),
        ('other', 'Other'),
    ]
    policy_name = models.CharField(max_length=200)
    provider_name = models.CharField(max_length=200)
    description = models.TextField()
    policy_type = models.CharField(max_length=10, choices=POLICY_CHOICES, default='health')

# --- ADD THIS NEW FIELD (Your Suggestion #4) ---
    coverage_summary = models.TextField(blank=True, help_text="A simple, non-technical summary of coverage.")
        
    def __str__(self):
        return self.policy_name
    

class PlaceCategory(models.Model):
    """
    Categories for places, e.g., "Park", "Museum", "Community Center"
    This is better than a ChoiceField because staff can add new ones.
    """
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Place Categories"

    def __str__(self):
        return self.name  

class PlaceToVisit(models.Model):
    CATEGORY_CHOICES = [
        ('park', 'Park'),
        ('museum', 'Museum'),
        ('club', 'Community Club'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=255)
    # name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    # category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')
    category = models.ForeignKey(PlaceCategory, on_delete=models.SET_NULL, null=True, blank=True) # <-- ADD THIS
    is_wheelchair_accessible = models.BooleanField(default=False)
    has_restrooms = models.BooleanField(default=False)
    has_seating = models.BooleanField(default=False)

    # --- ADD THIS NEW FIELD ---
        # This will be the main "card" image
    main_image = models.ImageField(
        upload_to='places/main/', 
        null=True, 
        blank=True
    )
        # --- END OF NEW FIELD ---

    def __str__(self):
        return self.name

# --- THIS IS THE UPDATED/REFACTORED MODEL (Step 2) ---
# 
class LearningResource(models.Model):
    """
    Learning content tailored to senior interests.
    This model now supports external links, uploaded files, and difficulty levels.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner (Easy)'),
        ('intermediate', 'Intermediate (Moderate)'),
        ('advanced', 'Advanced (Challenging)'),
    ]
    CONTENT_CHOICES = [
        ('article', 'Article / Guide'),
        ('video', 'Video'),
        ('pdf', 'Downloadable PDF'),
        ('tutorial', 'Interactive Tutorial'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Links to a Hobby (for personalization)
    category = models.ForeignKey(
        Hobby, 
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True,
        related_name="learning_resources"
    )
    
    # --- NEW FIELDS FOR CONTENT & TRACKING ---
    content_type = models.CharField(max_length=10, choices=CONTENT_CHOICES, default='article')
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default='beginner') # New field
    
    # The actual content can be a link OR an uploaded file
    external_link = models.URLField(
        max_length=500, 
        blank=True, 
        help_text="Link for videos or external articles (e.g., YouTube URL)"
    )
    uploaded_file = models.FileField(
        upload_to='learning/files/', 
        blank=True, 
        null=True,
        help_text="Upload a PDF or document"
    )

    def __str__(self):
        return self.title

# --- THIS IS THE NEW MODEL (Step 1) ---
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Link this event directly to a Hobby
    hobby = models.ForeignKey(
        Hobby, 
        on_delete=models.CASCADE, # If hobby is deleted, delete its events
        related_name="events"
    )
    
    location = models.CharField(max_length=300)
    event_date = models.DateTimeField()
    
    # Track who created this event (a staff member)
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, # Keep event if staff account is deleted
        null=True,
        limit_choices_to={'is_staff': True} # Only staff can be creators
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class PlaceImage(models.Model):
    
        
        """
        A gallery image for a PlaceToVisit.
        Each PlaceToVisit can have MANY PlaceImages.
        """
        place = models.ForeignKey(
            PlaceToVisit, 
            on_delete=models.CASCADE, 
            related_name='gallery_images'
        )
        image = models.ImageField(upload_to='places/gallery/')
        caption = models.CharField(max_length=255, blank=True)
        
        def __str__(self):
            return f"Image for {self.place.name}"
# --new insurance model--
class UserInsurancePolicy(models.Model):
        """
        A personal insurance policy uploaded and managed by a senior citizen.
        """
        POLICY_CHOICES = [
            ('health', 'Health'),
            ('life', 'Life'),
            ('auto', 'Auto'),
            ('home', 'Home/Renters'),
            ('travel', 'Travel'),
            ('other', 'Other'),
        ]
        
        PREMIUM_FREQUENCY_CHOICES = [
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('annually', 'Annually'),
            ('one-time', 'One-Time'),
        ]

        # This links the policy to a specific user
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE,
            related_name="insurance_policies"
        )
        
        # --- Fields from your Suggestion #1 ---
        policy_name = models.CharField(max_length=255)
        policy_number = models.CharField(max_length=255, blank=True)
        provider_name = models.CharField(max_length=255)
        coverage_type = models.CharField(max_length=10, choices=POLICY_CHOICES, default='health')
        
        start_date = models.DateField(null=True, blank=True)
        expiry_date = models.DateField(null=True, blank=True)
        
        premium_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        premium_frequency = models.CharField(max_length=10, choices=PREMIUM_FREQUENCY_CHOICES, default='monthly')

        # --- Field from your Suggestion #3 ---
        policy_document = models.FileField(
            upload_to='policies/documents/', 
            null=True, 
            blank=True,
            help_text="Upload a scanned copy of your policy (PDF, JPG, etc.)"
        )
        
        # --- Field from your Suggestion #4 ---
        coverage_summary = models.TextField(blank=True, help_text="Your personal notes or summary of coverage.")

        def __str__(self):
            return f"{self.user.username}'s {self.policy_name}"

    # --- END OF NEW MODEL ---

# --- ADD THIS ENTIRE NEW MODEL ---

class Doctor(models.Model):
    """
    Detailed profile for individual doctors affiliated with hospitals.
    """
    
    # Specialties based on common senior needs
    SPECIALTY_CHOICES = [
        ('cardio', 'Cardiology'),
        ('geriatrics', 'Geriatrics'),
        ('ortho', 'Orthopedics'),
        ('opthal', 'Ophthalmology'),
        ('dental', 'Dentistry'),
        ('gp', 'General Practitioner'),
        ('neuro', 'Neurology'),
    ]

    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    
    # Affiliation (linking Doctor to a Hospital)
    hospital_affiliation = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affiliated_doctors"
    )
    
    # Profile details (Your Suggestions #2)
    contact_phone = models.CharField(max_length=20)
    years_experience = models.IntegerField(default=5)
    languages_spoken = models.CharField(max_length=255, blank=True, help_text="Comma-separated list (e.g., Hindi, English)")
    
    # Optional Profile Image
    profile_photo = models.ImageField(
        upload_to='doctors/profiles/',
        null=True,
        blank=True
    )
    
    # Visiting hours would be complex, so we'll use a simple text field for now:
    visiting_hours = models.TextField(
        blank=True,
        help_text="e.g., Mon, Wed, Fri: 10 AM - 2 PM"
    )

    def __str__(self):
        return f"Dr. {self.name} ({self.get_specialty_display()})"

# --- END OF NEW MODEL ---


# 
class LearningProgress(models.Model):
    """
    Tracks the completion status of a resource for a specific user.
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('bookmarked', 'Bookmarked')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    resource = models.ForeignKey(
        LearningResource,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Ensure a user can only have one status per resource
    class Meta:
        unique_together = ('user', 'resource')
        verbose_name_plural = "Learning Progress Records"

    def __str__(self):
        return f"{self.user.username}'s progress on {self.resource.title}"

# --- END OF NEW MODEL ---

# ... (rest of your models above) ...

class Game(models.Model):
    """
    Curated list of games for mental stimulation and social play.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    TYPE_CHOICES = [
        ('puzzle', 'Puzzle/Memory'),
        ('board', 'Board Game'),
        ('word', 'Word Game'),
    ]

    # --- MAKE SURE THESE LINES ARE INDENTED INSIDE THE CLASS ---
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    game_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='puzzle')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    # Link to the actual game code (will be a URL path)
    game_url = models.CharField(
        max_length=200, 
        help_text="The URL path where the game is located (e.g., /games/memory/)"
    )
    
    # Accessibility Features
    is_high_contrast = models.BooleanField(default=True)
    is_large_text = models.BooleanField(default=True)
    is_multiplayer_ready = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


    # ... (after Game model) ...

class GameSession(models.Model):
    """
    Tracks a user's session, score, and outcome for a game.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    
    # Outcome tracking
    OUTCOME_CHOICES = [
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('draw', 'Draw'),
        ('quit', 'Quit/Incomplete'),
    ]
    outcome = models.CharField(max_length=10, choices=OUTCOME_CHOICES, default='quit')

    def __str__(self):
        return f"{self.user.username}'s session on {self.game.name}"

# --- END OF NEW MODEL ---