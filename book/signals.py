from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Book

RECIPIENT_LIST = ["sahitndaheu@gmail.com"]
SITE_DOMAIN = "localhost:8000"


@receiver(post_save, sender=Book)
def book_saved(sender, instance, created, **kwargs):
    if created:
        action = "created"
        action_label = _("Nouveau livre ajouté")
        print("[SIGNAL]: Un livre cree ", instance.title, instance.isbn)
    else:
        action = "updated"
        action_label = _("Livre modifié")
        print("[SIGNAL]: Un livre modifie ", instance.title, instance.isbn)

    subject = f"{action_label} — {instance.title}"

    context = {
        "book": instance,
        "action": action,
        "action_label": action_label,
        "site_domain": SITE_DOMAIN,
    }

    html = render_to_string("book/mail.html", context)
    text = render_to_string("book/mail.txt", context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=RECIPIENT_LIST,
    )
    email.attach_alternative(html, "text/html")
    email.send()
@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    action = "deleted"
    action_label = _("Livre supprimé")
    print("[SIGNAL]: Un livre supprime ", instance.title, instance.isbn)

    subject = f"{action_label} — {instance.title}"

    context = {
        "book": instance,
        "action": action,
        "action_label": action_label,
        "site_domain": SITE_DOMAIN,
    }

    html = render_to_string("book/mail.html", context)
    text = render_to_string("book/mail.txt", context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=RECIPIENT_LIST,
    )
    email.attach_alternative(html, "text/html")
    email.send()
