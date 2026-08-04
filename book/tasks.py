from celery import shared_task
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext as _
from .models import Book

RECIPIENT_LIST = ["cuba7843@gmail.com"]
SITE_DOMAIN = "localhost:8000"

@shared_task
def book_notifications(id_b,action):

    if action == "created":
        action_label = _("Nouveau livre ajouté")
    elif action == "deleted":
        action_label = _("Livre supprimé")
    else:
        action_label = _("Livre modifié")

    book = get_object_or_404(Book, id=id_b)
    available_copies = book.total_copies - book.unavailable_copies
    subject = f"{action_label} — {book.title}"

    context = {
        "book": book,
        "available_copies": available_copies,
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
