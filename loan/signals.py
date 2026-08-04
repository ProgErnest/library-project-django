from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.emails import send_personalized_email

from .models import Loan

RECIPIENT_LIST = ["client@gmail.com"]
SITE_DOMAIN = "localhost:8000"


@receiver(post_save, sender=Loan)
def loan_saved(sender, instance, created, **kwargs):
    if created:
        action = "created"
        action_label = _("Nouvel emprunt créé")
        print("[SIGNAL]: Un emprunt cree ", instance.borrower, instance.book.title)
    else:
        action = "updated"
        action_label = _("Emprunt modifié")
        print("[SIGNAL]: Un emprunt modifie ", instance.borrower, instance.book.title)

    subject = f"{action_label} — {instance.book.title} ({instance.borrower})"

    context = {
        "loan": instance,
        "action": action,
        "action_label": action_label,
        "site_domain": SITE_DOMAIN,
    }

    send_personalized_email(
        subject=subject,
        context=context,
        html_template="loan/email.html",
        text_template="loan/email.txt",
        recipient_list=RECIPIENT_LIST,
    )


@receiver(post_delete, sender=Loan)
def loan_deleted(sender, instance, **kwargs):
    action = "deleted"
    action_label = _("Emprunt supprimé")
    print("[SIGNAL]: Un emprunt supprime ", instance.borrower, instance.book.title)

    subject = f"{action_label} — {instance.book.title} ({instance.borrower})"

    context = {
        "loan": instance,
        "action": action,
        "action_label": action_label,
        "site_domain": SITE_DOMAIN,
    }

    send_personalized_email(
        subject=subject,
        context=context,
        html_template="loan/email.html",
        text_template="loan/email.txt",
        recipient_list=RECIPIENT_LIST,
    )
