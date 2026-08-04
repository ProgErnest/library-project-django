from celery import shared_task
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext as _
from .models import Loan

RECIPIENT_LIST = ["cuba7843@gmail.com"]
SITE_DOMAIN = "localhost:8000"

@shared_task
def loan_mail_notification(id_l,action):

    if action == "created":
        action_label = _("Nouvel emprunt créé")
    elif action == "deleted":
        action_label = _("Emprunt supprimé")
    else:
        action_label = _("Emprunt modifié")

    loan = get_object_or_404(Loan, id_l)
    subject = f"{action_label} — {loan.book.title} ({loan.borrower})"

    context = {
        "loan": loan,
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
