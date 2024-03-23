from django.apps import AppConfig


class NearApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'near_api_v1'

    def ready(self):
        import near_api_v1.signals
