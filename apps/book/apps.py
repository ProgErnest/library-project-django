from django.apps import AppConfig


class BookConfig(AppConfig):
    name = 'apps.book'

    def ready(self):
        import apps.book.signals