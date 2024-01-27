from django.apps import AppConfig


class UseractivityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "useractivity"

    def ready(self):
        import useractivity.signals
