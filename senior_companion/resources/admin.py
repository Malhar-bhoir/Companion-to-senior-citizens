from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PlaceToVisit, LearningResource, Hospital, InsurancePolicy
from .models import PlaceToVisit, LearningResource, Hospital, InsurancePolicy, Event, PlaceCategory,UserInsurancePolicy , Doctor , LearningProgress , Game, GameSession

# Register your new models
admin.site.register(PlaceToVisit)
admin.site.register(LearningResource)
admin.site.register(Hospital)
admin.site.register(InsurancePolicy)
admin.site.register(Event)
admin.site.register(PlaceCategory)
admin.site.register(UserInsurancePolicy)
admin.site.register(Doctor) # <-- ADD THIS NEW LINE
admin.site.register(LearningProgress) 
admin.site.register(Game) # <-- ADD THIS
admin.site.register(GameSession) # <-- ADD THIS