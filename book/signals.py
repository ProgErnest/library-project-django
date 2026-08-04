from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.emails import send_personalized_email

from .models import Book

RECIPIENT_LIST = ["client@gmail.com"]
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

    send_personalized_email(
        subject=subject,
        context=context,
        html_template="book/mail.html",
        text_template="book/mail.txt",
        recipient_list=RECIPIENT_LIST,
    )


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

    send_personalized_email(
        subject=subject,
        context=context,
        html_template="book/mail.html",
        text_template="book/mail.txt",
        recipient_list=RECIPIENT_LIST,
    )
