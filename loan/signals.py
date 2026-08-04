from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _


from .models import Loan

RECIPIENT_LIST = ["cuba7843@gmail.com"]
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
    html = render_to_string("loan/email.html", context)
    text = render_to_string("loan/email.txt", context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=RECIPIENT_LIST,
    )
    email.attach_alternative(html, "text/html")
    email.send()

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

    html = render_to_string("loan/email.html", context)
    text = render_to_string("loan/email.txt", context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=RECIPIENT_LIST,
    )
    email.attach_alternative(html, "text/html")
    email.send()