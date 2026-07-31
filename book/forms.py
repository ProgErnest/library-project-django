from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from .models import Book

class CreateBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = [
            'title',
            'subtitle',
            'language',
            'genre',
            'isbn',
            'author',
            'num_pages',
            'available',
            'publication_date',
            'total_copies',
            'available_copies',
            'summary',
        ]
        localized_fields = ['publication_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Ex : Le Petit Prince'
            }),
            'subtitle': forms.TextInput(attrs={
                'placeholder': 'Ex : Le livre de la royaute'
            }),
            'language': forms.TextInput(attrs={
                'placeholder': 'Ex : French'
            }),
            'genre': forms.TextInput(attrs={
                'placeholder': 'Ex : Roman'
            }),
            'isbn': forms.TextInput(attrs={
                'placeholder': 'Ex : 978-3-16-148410-0'
            }),
            'num_pages': forms.NumberInput(attrs={
                'min': '1',
                'placeholder': 'Ex : 1488'
            }),
            'total_copies': forms.NumberInput(attrs={
                'min': '0',
                'placeholder': 'Ex : 5'
            }),
            'available_copies': forms.NumberInput(attrs={
                'min': '0',
                'placeholder': 'Ex : 4'
            }),
            'author': forms.Select(attrs={}),
            'available': forms.CheckboxInput(attrs={
                'checked': False
            }),
            'publication_date': forms.DateInput(attrs={
                'type': 'date',
            }),

        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError('Le titre est obligatoire.')
        if len(title) < 2:
            raise ValidationError('Le titre doit contenir au moins 2 caractères.')
        if len(title) > 100:
            raise ValidationError('Le titre ne peut pas dépasser 100 caractères.')
        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data.get('subtitle', '').strip()
        if subtitle and len(subtitle) > 100:
            raise ValidationError('Le sous-titre ne peut pas dépasser 100 caractères.')
        return subtitle

    def clean_language(self):
        language = self.cleaned_data.get('language', '').strip()
        if not language:
            raise ValidationError('La langue est obligatoire.')
        if len(language) < 2:
            raise ValidationError('La langue est trop courte.')
        return language.title()

    def clean_genre(self):
        genre = self.cleaned_data.get('genre', '').strip()
        if not genre:
            raise ValidationError('Le genre est obligatoire.')
        if len(genre) < 2:
            raise ValidationError('Le genre est trop court.')
        return genre.title()

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn', '').strip()
        if not isbn:
            raise ValidationError('L’ISBN est obligatoire.')
        if len(isbn) < 10 or len(isbn) > 17:
            raise ValidationError('L’ISBN doit contenir entre 10 et 17 caractères.')
        if not any(char.isdigit() for char in isbn):
            raise ValidationError('L’ISBN doit contenir au moins un chiffre.')
        return isbn.upper()

    def clean_num_pages(self):
        num_pages = self.cleaned_data.get('num_pages')
        if num_pages is not None and num_pages < 1:
            raise ValidationError('Le nombre de pages doit être supérieur à 0.')
        if num_pages is not None and num_pages > 5000:
            raise ValidationError('Le nombre de pages ne peut pas dépasser 5000.')
        return num_pages

    def clean_publication_date(self):
        publication_date = self.cleaned_data.get('publication_date')
        if publication_date and publication_date > date.today():
            raise ValidationError('La date de publication ne peut pas être dans le futur.')
        return publication_date

    def clean_total_copies(self):
        total_copies = self.cleaned_data.get('total_copies')
        if total_copies is not None and total_copies < 0:
            raise ValidationError('Le nombre total d’exemplaires ne peut pas être négatif.')
        if total_copies is not None and total_copies > 1000:
            raise ValidationError('Le nombre total d’exemplaires ne peut pas dépasser 1000.')
        return total_copies

    def clean_available_copies(self):
        available_copies = self.cleaned_data.get('available_copies')
        total_copies = self.cleaned_data.get('total_copies')
        if available_copies is not None and available_copies < 0:
            raise ValidationError('Le nombre d’exemplaires disponibles ne peut pas être négatif.')
        if total_copies is not None and available_copies is not None and available_copies > total_copies:
            raise ValidationError('Les exemplaires disponibles ne peuvent pas dépasser le total.')
        return available_copies

    def clean_summary(self):
        summary = self.cleaned_data.get('summary', '').strip()
        if summary and len(summary) < 20:
            raise ValidationError('Le résumé doit contenir au moins 20 caractères.')
        return summary

    def clean(self):
        cleaned_data = super().clean()
        total_copies = cleaned_data.get('total_copies')
        available_copies = cleaned_data.get('available_copies')

        if total_copies is not None and available_copies is None:
            cleaned_data['available_copies'] = total_copies

        return cleaned_data
