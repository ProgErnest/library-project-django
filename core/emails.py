from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_personalized_email(
    *,
    subject: str,
    context: dict,
    html_template: str,
    text_template: str,
    recipient_list: list[str],
    from_email: str | None = None,
) -> int:
    """Envoie un email personnalisé avec deux alternatives : HTML et texte.

    Utilise ``EmailMultiAlternatives`` pour que les clients de messagerie
    puissent afficher soit la version HTML soit la version texte brut.

    Retourne le nombre de messages envoyés (via ``send()``).
    """
    # Rend la version HTML et la version texte directement depuis le contexte
    html_message = render_to_string(html_template, context)
    text_message = render_to_string(text_template, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )

    # Attache la version HTML comme alternative au corps texte
    email.attach_alternative(html_message, "text/html")

    return email.send()
