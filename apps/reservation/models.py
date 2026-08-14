from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# from book.models import Book

# Create your models here.

class Reservation(models.Model):
    book = models.ForeignKey(
        "book.Book",
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("book")
    )
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("reader")
    )
    reservation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name=_("active"))

    class Meta:
        verbose_name = _("reservation")
        verbose_name_plural = _("reservations")
        ordering = ["-reservation_date"]
        indexes = [
            models.Index(fields=["-reservation_date", "book"]),
            models.Index(fields=["-reservation_date", "reader"]),
            models.Index(fields=["-reservation_date", "is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "reader"],
                condition=models.Q(is_active=True),
                name="unique_active_reservation_per_reader"
            )
        ]

    def __str__(self):
        return f"{self.reader.username} → {self.book.title}"

    # def get_absolute_url(self):
    #     return reverse("reservation:detail", kwargs={"pk": self.pk})