from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        lector, _ = Group.objects.get_or_create(name='lector')
        permissions_lector = Permission.objects.filter(content_type__app_label__in=['reservation', 'loan', 'review']).exclude(codename__startswith='change_').exclude(codename__startswith='delete_')
        lector.permissions.set(permissions_lector)
        self.stdout.write(f"Lecteur : {permissions_lector.count()} permissions assignées")
        librerian, _ = Group.objects.get_or_create(name='librarian')
        permissions = Permission.objects.filter(content_type__app_label__in=['book', 'loan', 'author', 'reservation'])
        librerian.permissions.set(permissions)
        self.stdout.write(f"Librarian : {permissions.count()} permissions assignées")