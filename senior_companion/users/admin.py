from django.contrib import admin
from .models import CustomUser, Profile, Hobby

# We'll just register our models for now.
# This lets us see and edit them in the /admin dashboard.

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Hobby)