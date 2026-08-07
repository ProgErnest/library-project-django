from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from .models import Book, Genre


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "subtitle",
            "author",
            "genre_id",
            "language",
            "isbn",
            "num_pages",
            "publication_date",
            "cover",
            "total_copies",
            "summary",
        ]
        localized_fields = ["publication_date"]
        labels = {
            "title": _("Title"),
            "subtitle": _("Subtitle"),
            "author": _("Author"),
            "language": _("Language"),
            "genre_id": _("Genre"),
            "isbn": _("ISBN"),
            "num_pages": _("Number of pages"),
            "publication_date": _("Publication date"),
            "cover": _("Cover"),
            "total_copies": _("Total copies"),
            "summary": _("Summary"),
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": _("Example: Le Petit Prince")}),
            "subtitle": forms.TextInput(attrs={"placeholder": _("Example: The royal book")}),
            "language": forms.TextInput(attrs={"placeholder": _("Example: French")}),
            "genre_id": forms.Select(attrs={}),
            "isbn": forms.TextInput(attrs={"placeholder": _("Example: 978-3-16-148410-0")}),
            "num_pages": forms.NumberInput(attrs={"min": "1", "placeholder": _("Example: 1488")}),
            "total_copies": forms.NumberInput(attrs={"min": "0", "placeholder": _("Example: 5")}),
            "author": forms.Select(attrs={}),
            "cover": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "publication_date": forms.DateInput(attrs={"type": "date"}),
        }




    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise ValidationError(_("The title is required."))
        if len(title) < 2:
            raise ValidationError(_("The title must contain at least 2 characters."))
        if len(title) > 100:
            raise ValidationError(_("The title cannot exceed 100 characters."))
        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data.get("subtitle", "").strip()
        if subtitle and len(subtitle) > 100:
            raise ValidationError(_("The subtitle cannot exceed 100 characters."))
        return subtitle

    def clean_language(self):
        language = self.cleaned_data.get("language", "").strip()
        if not language:
            raise ValidationError(_("The language is required."))
        if len(language) < 2:
            raise ValidationError(_("The language is too short."))
        return language.title()

    def clean_genre_id(self):
        genre_id = self.cleaned_data.get("genre_id")
        if not genre_id:
            raise ValidationError(_("The genre is required."))
        return genre_id

    def clean_isbn(self):
        isbn = self.cleaned_data.get("isbn", "").strip()
        if not isbn:
            raise ValidationError(_("The ISBN is required."))
        if len(isbn) < 10 or len(isbn) > 17:
            raise ValidationError(_("The ISBN must contain between 10 and 17 characters."))
        if not any(char.isdigit() for char in isbn):
            raise ValidationError(_("The ISBN must contain at least one digit."))
        return isbn.upper()

    def clean_num_pages(self):
        num_pages = self.cleaned_data.get("num_pages")
        if num_pages is not None and num_pages < 1:
            raise ValidationError(_("The number of pages must be greater than 0."))
        if num_pages is not None and num_pages > 5000:
            raise ValidationError(_("The number of pages cannot exceed 5000."))
        return num_pages

    def clean_publication_date(self):
        publication_date = self.cleaned_data.get("publication_date")
        if publication_date and publication_date > date.today():
            raise ValidationError(_("The publication date cannot be in the future."))
        return publication_date

    def clean_total_copies(self):
        total_copies = self.cleaned_data.get("total_copies")
        if total_copies is not None and total_copies < 0:
            raise ValidationError(_("The total number of copies cannot be negative."))
        if total_copies is not None and total_copies > 1000:
            raise ValidationError(_("The total number of copies cannot exceed 1000."))
        return total_copies

    # def clean_available_copies(self):
    #     available_copies = self.cleaned_data.get("available_copies")
    #     total_copies = self.cleaned_data.get("total_copies")
    #     if available_copies is not None and available_copies < 0:
    #         raise ValidationError(_("The number of available copies cannot be negative."))
    #     if total_copies is not None and available_copies is not None and available_copies > total_copies:
    #         raise ValidationError(_("Available copies cannot exceed the total."))
    #     return available_copies

    def clean_summary(self):
        summary = self.cleaned_data.get("summary", "").strip()
        if summary and len(summary) < 20:
            raise ValidationError(_("The summary must contain at least 20 characters."))
        return summary

    def clean(self):
        cleaned_data = super().clean()
        total_copies = cleaned_data.get("total_copies")
        # available_copies = cleaned_data.get("available_copies")
        return cleaned_data

    def save(self, commit=True):
        book = super().save(commit=False)
        # Synchronise le champ texte `genre` avec la catégorie sélectionnée (genre_id)
        if book.genre_id:
            book.genre = book.genre_id.name
        if commit:
            book.save()
            self.save_m2m()
        return book

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name", "description"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }
        widgets = {
            "name": forms.TextInput(attrs={}),
            "description": forms.Textarea(attrs={},)
        }
    def save(self, commit=True):
        genre = super().save(commit=False)
        genre.slug = slugify(genre.name)
        if commit:
            genre.save()
        return genre