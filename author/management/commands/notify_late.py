# # core/management/commands/rappel_retards.py
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from author.models import Loan

# class Command(BaseCommand):
#     help = "Envoie un rappel pour tous les emprunts en retard non rendus"

#     def handle(self, *args, **options):
#         aujourdhui = timezone.localdate()
#         retards = Loan.objects.filter(
#             return_date__lt=aujourdhui,
#             effective_return_date__isnull=True,
#         )
#         for loan in retards:
#             self.stdout.write(f"[RAPPEL] {loan.borrower} — « {loan.book.title} » en retard depuis le {loan.return_date}")
#             # branche ici ton envoi d'email du Jour 5 (envoyer_confirmation_emprunt-like)

#         self.stdout.write(self.style.SUCCESS(f"{retards.count()} rappel(s) traité(s)."))