from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from core.emails import send_personalized_email

from .models import Author

RECIPIENT_LIST = ["cuba7843@gmail.com"]
SITE_DOMAIN = "localhost:8000"


@receiver(post_save, sender=Author)
def author_saved(sender, instance, created, **kwargs):
    if created:
        action = "created"
        action_label = _("Nouvel auteur ajouté")
        print("[SIGNAL]: Un auteur cree ", instance.surname, instance.name)
    else:
        action = "updated"
        action_label = _("Auteur modifié")
        print("[SIGNAL]: Un auteur modifie ", instance.surname, instance.name)

    subject = f"{action_label} — {instance.name} {instance.surname}"

    context = {
        "author": instance,
        "action": action,
        "action_label": action_label,
        "site_domain": SITE_DOMAIN,
    }

    html = render_to_string("author/author_email.html", context)
    text = render_to_string("author/author_email.txt", context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=RECIPIENT_LIST,
    )
    email.attach_alternative(html, "text/html")
    email.send()


@receiver(post_delete, sender=Author)
def author_deleted(sender, instance, **kwargs):
    action = "deleted"
    action_label = _("Auteur supprimé")
    print("[SIGNAL]: Un auteur supprime ", instance.surname, instance.name)

    subject = f"{action_label} — {instance.name} {instance.surname}"

    context = {
        "author": instance,
        "action": action,
        "action_label": action_label,
        "site_domain": SITE_DOMAIN,
    }

    html = render_to_string("author/author_email.html", context)
    text = render_to_string("author/author_email.txt", context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=RECIPIENT_LIST,
    )

    email.attach_alternative(html, "text/html")
    email.send()