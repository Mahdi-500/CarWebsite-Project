from django.apps import AppConfig

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        import os
        if os.environ.get("RUN_MAIN") == "true":
            from .my_apps import schedular
            schedular.start()