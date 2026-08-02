from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from book.models import Book
from .models import Loan


class LoanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(available=True)

    return_date = forms.DateField(
        label=_("Return date"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Loan
        fields = ["book", "borrower", "loan_date", "return_date", "effective_return_date"]
        labels = {
            "book": _("Book"),
            "borrower": _("Borrower"),
            "loan_date": _("Loan date"),
            "return_date": _("Return date"),
            "effective_return_date": _("Effective return date"),
        }
    def clean_borrower(self):
        borrower = self.cleaned_data.get("borrower", "").strip()
        if not borrower:
            raise ValidationError(_("The borrower name is required."))
        if len(borrower) < 2:
            raise ValidationError(_("The borrower name is too short."))
        if len(borrower) > 100:
            raise ValidationError(_("The borrower name cannot exceed 100 characters."))
        if any(char.isdigit() for char in borrower):
            raise ValidationError(_("The borrower name must not contain digits."))
        return borrower.title()

    def clean(self):
        
        cleaned_data = super().clean()
        return_date = cleaned_data.get("return_date")
        effective_return_date = cleaned_data.get("effective_return_date")
        book = cleaned_data.get("book")

        if book and not book.available_copies:
            raise ValidationError(_("This book no longer has copies available for a loan."))

        if return_date and effective_return_date and effective_return_date < return_date:
            raise ValidationError(_("The effective return date cannot be earlier than the planned return date."))

        return cleaned_data
