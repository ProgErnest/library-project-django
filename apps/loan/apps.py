from django.apps import AppConfig


class LoanConfig(AppConfig):
    name = 'apps.loan'

    def ready(self):
        import apps.loan.signals