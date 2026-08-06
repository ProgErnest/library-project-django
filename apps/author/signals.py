from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from core.emails import send_personalized_email
from django.db import transaction 
from .models import Author
from .tasks import send_authors_mail
RECIPIENT_LIST = ["cuba7843@gmail.com"]
SITE_DOMAIN = "localhost:8000"


@receiver(post_save, sender=Author)
def author_saved(sender, instance, created, **kwargs):

    action = "created" if created else "updated"
    # if created:
    #     action = "created"
    #     action_label = _("Nouvel auteur ajouté")
    #     print("[SIGNAL]: Un auteur cree ", instance.surname, instance.name)
    # else:
    #     action = "updated"
    #     action_label = _("Auteur modifié")
    #     print("[SIGNAL]: Un auteur modifie ", instance.surname, instance.name)

    transaction.on_commit(
        lambda:send_authors_mail.delay(instance.id, action)
    )



@receiver(post_delete, sender=Author)
def author_deleted(sender, instance, **kwargs):
    action = "deleted"
    transaction.on_commit(
        lambda:send_authors_mail.delay(instance.id, action)
    )