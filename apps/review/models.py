from django.db import models

# Create your models here.
# apps/review/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Review(models.Model):
    book = models.ForeignKey(
        "book.Book",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("book")
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("reviewer")
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name=_("rating")
    )
    comment = models.TextField(blank=True, verbose_name=_("comment"))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("avis")
        verbose_name_plural = _("avis")
        unique_together = [("book", "reviewer")]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.reviewer.username} → {self.book.title} ({self.rating}/5)"

    def get_absolute_url(self):
        return self.book.get_absolute_url()