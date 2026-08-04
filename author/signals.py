from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.emails import send_personalized_email

from .models import Author

RECIPIENT_LIST = ["client@gmail.com"]
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

    send_personalized_email(
        subject=subject,
        context=context,
        html_template="author/author_email.html",
        text_template="author/author_email.txt",
        recipient_list=RECIPIENT_LIST,
    )


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

    send_personalized_email(
        subject=subject,
        context=context,
        html_template="author/author_email.html",
        text_template="author/author_email.txt",
        recipient_list=RECIPIENT_LIST,
    )
