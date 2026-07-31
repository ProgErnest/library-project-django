from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from book.models import Book
from .models import Loan

class LoanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(available=True)

    return_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Loan
        fields = ['book', 'borrower', 'return_date', 'effective_return_date']

    def clean_borrower(self):
        borrower = self.cleaned_data.get('borrower', '').strip()
        if not borrower:
            raise ValidationError('Le nom de l’emprunteur est obligatoire.')
        if len(borrower) < 2:
            raise ValidationError('Le nom de l’emprunteur est trop court.')
        if len(borrower) > 100:
            raise ValidationError('Le nom de l’emprunteur ne peut pas dépasser 100 caractères.')
        if any(char.isdigit() for char in borrower):
            raise ValidationError('Le nom de l’emprunteur ne doit pas contenir de chiffres.')
        return borrower.title()

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        if return_date and return_date < date.today():
            raise ValidationError('La date de retour ne peut pas être dans le passé.')
        return return_date

    def clean_effective_return_date(self):
        effective_return_date = self.cleaned_data.get('effective_return_date')
        if effective_return_date and effective_return_date < date.today():
            raise ValidationError('La date de retour effective ne peut pas être dans le passé.')
        return effective_return_date

    def clean(self):
        cleaned_data = super().clean()
        return_date = cleaned_data.get('return_date')
        effective_return_date = cleaned_data.get('effective_return_date')
        book = cleaned_data.get('book')

        if book and not book.available_copies:
            raise ValidationError('Ce livre n’a plus d’exemplaires disponibles pour un emprunt.')

        if return_date and effective_return_date and effective_return_date < return_date:
            raise ValidationError('La date de retour effective ne peut pas être antérieure à la date de retour prévue.')

        return cleaned_data
