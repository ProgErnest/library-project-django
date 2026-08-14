from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from apps.book.models import Book


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans", verbose_name=_("Book"))
    borrower = models.CharField(_("Borrower"), max_length=50, blank=True, null=True)
    borrower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans", verbose_name=_("Borrower"), blank=True, null=True)
    loan_date = models.DateField(_("Loan date"), auto_now=False, auto_now_add=False, default=timezone.now)
    return_date = models.DateField(_("Return date"), auto_now=False, auto_now_add=False)
    effective_return_date = models.DateField(_("Effective return date"), null=True, blank=True, auto_now=False, auto_now_add=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.book.unavailable_copies += 1
            self.book.save()
        else:
            if self.effective_return_date and self.effective_return_date <= timezone.now().date():
                self.book.unavailable_copies -= 1
                self.book.save()

    class Meta:
        verbose_name = _("loan")
        verbose_name_plural = _("loans")
        ordering = ["-loan_date"]
        permissions = [
            ("view_all_loans", _("Can view all loans")),
        ]
        indexes = [
            models.Index(fields=["-loan_date", "book"]),
            models.Index(fields=["-loan_date", "borrower_id"]),
        ]
    @property
    def status(self):
        if self.effective_return_date:
            return _("Returned")
        if timezone.localdate() > self.return_date:
            return _("Late")
        return _("In progress")

    def __str__(self):
        
        return f"{self.book.title} {_('borrowed by')} {self.borrower_id.username if self.borrower_id else _('Unknown borrower')}"
