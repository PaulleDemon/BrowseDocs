from django.apps import AppConfig

class DocsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'docsapp'

    def ready(self) -> None:
        from . import singnals
        return super().ready()