from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms_api.apps.core'

    def ready(self):
        import lms_api.resources.signals.user_handler