from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db import transaction

from .models import Book
from .tasks import book_notifications
RECIPIENT_LIST = ["sahitndaheu@gmail.com"]
SITE_DOMAIN = "localhost:8000"


@receiver(post_save, sender=Book)
def book_saved(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    transaction.on_commit(
        lambda: book_notifications.delay(instance.id, action)
    )

@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    action = "deleted"
    transaction.on_commit(
        lambda: book_notifications.delay(instance.id, action)
    )