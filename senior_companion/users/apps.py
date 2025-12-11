from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # This is the line we add
        # It imports our signals.py file so the signals get registered
        import users.signals