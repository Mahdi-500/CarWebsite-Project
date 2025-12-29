from django.apps import AppConfig

class CarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Car'

    # def ready(self):
    #     import os
    #     if os.environ.get("RUN_MAIN") == "true":
    #         from .my_apps import schedular
    #         schedular.start()