from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Author(models.Model):

    name = models.CharField(_("name"), max_length=50)
    surname = models.CharField(_("surname"), max_length=50)
    birthday = models.DateField(_("birthday"), auto_now=False, auto_now_add=False)
    nationality = models.CharField(max_length=100)
    biography = models.TextField()

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name
