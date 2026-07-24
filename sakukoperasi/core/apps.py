from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    label = 'member'

    def ready(self):
        """Load signals saat app startup."""
        import core.signals  # noqa: F401
