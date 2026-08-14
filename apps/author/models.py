from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    surname = models.CharField(_("Surname"), max_length=50)
    birthday = models.DateField(_("Birthday"), auto_now=False, auto_now_add=False)
    nationality = models.CharField(_("Nationality"), max_length=100)
    biography = models.TextField(_("Biography"), blank=True, null=True)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["surname"]),
            models.Index(fields=["nationality"]),
        ]

    def __str__(self):
        return f"{self.name} {self.surname}".strip()
