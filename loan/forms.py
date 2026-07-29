from django import forms
from book.models import Book
from .models import Loan

class LoanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(available=True)
    return_date = forms.DateField(
        widget= forms.DateInput(attrs = {'type': 'date'})
    )

    class Meta:
        model = Loan
        fields = ['book','borrower','return_date','effective_return_date']
