from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

#
# 1. Our Custom User Model
#
class CustomUser(AbstractUser):
    """
    We use the built-in `is_staff` field to identify Admins.
    A user with `is_staff=True` is a Staff Admin.
    A user with `is_staff=False` is a Senior Citizen.
    We can add more fields here later if we want.
    """
    email = models.EmailField(unique=True) # Make email the unique login
    
    # We will use email as the username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 'username' is still required for createsuperuser

    def __str__(self):
        return self.email

#
# 2. Our Hobby Model
#
class Hobby(models.Model):
    """
    A simple model to store a list of hobbies.
    e.g., "Gardening", "Reading", "Chess", "Cooking"
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

#
# 3. Our Profile Model
#
class Profile(models.Model):
    """
    This model stores all the *extra* information about a user.
    We link it to our CustomUser with a OneToOneField.
    This is a professional and clean way to separate auth from info.
    """
    
    # This is the link to the CustomUser.
    # If a User is deleted, their Profile is also deleted.
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    # A user can have many hobbies, and a hobby can belong to many users
    hobbies = models.ManyToManyField(Hobby, blank=True)
    
    # Our features from the abstract
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    # --- ADD THESE NEW FIELDS FOR HOME ADDRESS ---
    home_address_city = models.CharField(max_length=100, blank=True, verbose_name="Home City")
    home_address_state = models.CharField(max_length=100, blank=True, verbose_name="Home State/Region")
    
    
    companions = models.ManyToManyField(
        CustomUser, 
        related_name='companion_of', # A name to find who added this user
        blank=True
    )
    # --- END OF NEW FIELD ---
    def __str__(self):
        return f"{self.user.email}'s Profile"