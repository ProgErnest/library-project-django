from celery import shared_task
from .models import Author
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext as _
from smtplib import SMTPException
from socket import gaierror

RECIPIENT_LIST = ["cuba7843@gmail.com"]
SITE_DOMAIN = "localhost:8000"
@shared_task(
    bind = True,
    retry_kwargs={"max_retries": 5},
    )
def send_authors_mail(self, id_r,action):
    try:
        author = get_object_or_404(Author, id=id_r)

        if action == "created":
            action_label = _("Nouvel auteur ajouté")
        elif action == "deleted":
            action_label = _("Auteur supprimé")
        else:
            action_label = _("Auteur modifié")

        subject = f"{action_label} — {author.name} {author.surname}"
        context = {
            "author": author,
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

    except(gaierror, SMTPException) as e :
        raise self.retry(exec=e, countdown=60)