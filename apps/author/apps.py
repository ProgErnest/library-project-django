import os
from django.apps import AppConfig

class AuthorConfig(AppConfig):
    name = 'apps.author'

    def ready(self):
        import apps.author.signals
