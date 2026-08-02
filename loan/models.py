from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from book.models import Book


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans", verbose_name=_("Book"))
    borrower = models.CharField(_("Borrower"), max_length=50)
    loan_date = models.DateField(_("Loan date"), auto_now=False, auto_now_add=False, default=date.today)
    return_date = models.DateField(_("Return date"), auto_now=False, auto_now_add=False)
    effective_return_date = models.DateField(_("Effective return date"), null=True, blank=True, auto_now=False, auto_now_add=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.book.available_copies -= 1
            self.book.save()

    class Meta:
        verbose_name = _("loan")
        verbose_name_plural = _("loans")

    @property
    def status(self):
        if self.effective_return_date:
            return _("Returned")
        if date.today() > self.return_date:
            return _("Late")
        return _("In progress")

    def __str__(self):
        return f"{self.book.title} {_('borrowed by')} {self.borrower}"
