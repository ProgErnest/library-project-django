import os
from django.apps import AppConfig

class AuthorConfig(AppConfig):
    name = 'author'

    def ready(self):
        import author.signals
