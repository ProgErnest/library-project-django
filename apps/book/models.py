from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from apps.author.models import Author


class BookQuery(models.QuerySet):
    def available_only(self):
        return self.filter(available_copies__gt=0)


class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Slug"), max_length=50, unique=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ["name"]

    def __str__(self):    
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("genre_detail", kwargs={"slug": self.slug})

class Book(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    subtitle = models.CharField(_("Subtitle"), max_length=50)
    isbn = models.CharField(_("ISBN"), unique=True, max_length=50)
    language = models.CharField(_("Language"), max_length=50)
    genre = models.CharField(_("Genre"), max_length=50)
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name=_("Genre"), related_name="books")
    cover = models.ImageField(_("Cover"), upload_to="book_covers/%Y/%m/", null=True, blank=True)
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
    unavailable_copies = models.PositiveIntegerField(_("Unavailable copies"), default=0, blank=True, null=True)

    objects = BookQuery.as_manager()

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ["-publication_date"]



    def __str__(self):
        return f"{self.title} - {self.total_copies - self.unavailable_copies} / {self.total_copies}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("book_detail", kwargs={"pk": self.pk})
