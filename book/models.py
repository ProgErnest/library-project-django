from django.db import models
from django.utils.translation import gettext_lazy as _
from author.models import Author
# Create your models here.

class BookQuery(models.QuerySet):

    #Get all books that are available for a loan
    def available_only(self):
        return self.filter(available_copies__gt=0)


    
class Book(models.Model):

    title = models.CharField(_("title"), max_length = 50)
    subtitle = models.CharField(_("subtitle"), max_length = 50)
    isbn = models.CharField(_("isbn"), unique = True, max_length = 50)
    language = models.CharField(_("language"),max_length = 50)
    genre = models.CharField(_("genre"), max_length = 50)
    num_pages = models.PositiveIntegerField(_("number of pages"))
    publication_date = models.DateField(_("publication date"))
    available = models.BooleanField(default = True)
    author = models.ForeignKey(Author, on_delete = models.SET_NULL, null = True,verbose_name = _("author"), related_name = "books")
    summary = models.TextField(_("summary"), null = True, blank = True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1, blank=True, null=True)

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

