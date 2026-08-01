from datetime import date

from django.db import models
from book.models import Book
# Create your models here.
class Loan(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrower = models.CharField(max_length=50)
    loan_date = models.DateField(auto_now=False, auto_now_add=True)
    return_date = models.DateField(auto_now=False, auto_now_add=False)
    effective_return_date = models.DateField(null=True, blank=True,auto_now=False, auto_now_add=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.book.available_copies -= 1
            self.book.save()

    class Meta:
        verbose_name = "loan"
        verbose_name_plural = "loans"

    @property
    def status(self):
        if self.effective_return_date:
            return "Rendu"
        if date.today() > self.return_date:
            return "En retard"
        return "En cours"

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower}"



