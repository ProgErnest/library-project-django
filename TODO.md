# TODO — Mails personnalisés multi-alternatives (HTML + texte)

## Objectif
Envoyer des emails personnalisés pour **toutes** les actions (création, modification, suppression) sur les **Livres (book)**, **Emprunts (loan)** et **Auteurs (author)**, avec deux alternatives : **HTML** et **texte**.

## Étapes
- [x] Analyser le projet (signals, modèles, templates, settings)
- [x] Créer le helper réutilisable `core/emails.py` (EmailMultiAlternatives avec HTML + texte)
- [x] Créer les templates HTML + texte pour **Author**
  - [x] `author/templates/author/author_email.html` (affiné)
  - [x] `author/templates/author/author_email.txt` (nouveau)
- [x] Créer les templates HTML + texte pour **Book**
  - [x] `book/templates/book/mail.html` (HTML)
  - [x] `book/templates/book/mail.txt` (nouveau)
- [x] Créer les templates HTML + texte pour **Loan**
  - [x] `loan/templates/loan/email.html` (nouveau)
  - [x] `loan/templates/loan/email.txt` (nouveau)
- [x] Mettre à jour `author/signals.py` (create/update/delete) avec multi-alternatives
- [x] Mettre à jour `book/signals.py` (create/update/delete) avec multi-alternatives
- [x] Mettre à jour `loan/signals.py` (create/update/delete) avec multi-alternatives
- [ ] Tester l'envoi multi-alternatives (Mailtrap)
