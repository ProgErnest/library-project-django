import os
from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'author'

    # def ready(self):
    #     import author.signals
    #     if os.environ.get("RUN_MAIN") == "true":
    #         from .scheduler import start_plannificator
    #         start_plannificator()