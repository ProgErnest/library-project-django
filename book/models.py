from django.db import models
from django.utils.translation import gettext_lazy as _

from author.models import Author


class BookQuery(models.QuerySet):
    def available_only(self):
        return self.filter(available_copies__gt=0)


class Book(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    subtitle = models.CharField(_("Subtitle"), max_length=50)
    isbn = models.CharField(_("ISBN"), unique=True, max_length=50)
    language = models.CharField(_("Language"), max_length=50)
    genre = models.CharField(_("Genre"), max_length=50)
    num_pages = models.PositiveIntegerField(_("Number of pages"))
    publication_date = models.DateField(_("Publication date"))
    available = models.BooleanField(_("Available"), default=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Author"),
        related_name="books",
    )
    summary = models.TextField(_("Summary"), null=True, blank=True)
    total_copies = models.PositiveIntegerField(_("Total copies"), default=1)
    available_copies = models.PositiveIntegerField(_("Available copies"), default=1, blank=True, null=True)

    objects = BookQuery.as_manager()

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.available_copies} / {self.total_copies}"

