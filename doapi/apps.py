from django.apps import AppConfig


class DoapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doapi"
    def ready(self):
        import doapi.schema