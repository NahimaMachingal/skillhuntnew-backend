from django.apps import AppConfig


class InterviewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interview'

    def ready(self):
        import interview.signals  # Import the signal handlers
