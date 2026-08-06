from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db import transaction
from .tasks import loan_mail_notification
from .models import Loan




@receiver(post_save, sender=Loan)
def loan_saved(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    transaction.on_commit(
        lambda: loan_mail_notification.delay(instance.id, action)
    )


@receiver(post_delete, sender=Loan)
def loan_deleted(sender, instance, **kwargs):
    action = "deleted"

    transaction.on_commit(
        lambda: loan_mail_notification.delay(instance.id, action)
    )
    