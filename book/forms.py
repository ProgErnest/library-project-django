from django import forms
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
