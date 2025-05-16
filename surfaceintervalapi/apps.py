from django.apps import AppConfig


class SurfaceintervalapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "surfaceintervalapi"

    def ready(self):
        import surfaceintervalapi.signals  # noqa: F401
