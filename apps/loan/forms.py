from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from apps.book.models import Book
from .models import Loan


class LoanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(available=True)

        if self.user is not None:
            self.fields["borrower_id"].label_from_instance = self._borrower_label
            if not self.user.is_staff:
                # Le staff peut choisir librement l'emprunteur parmi tous les utilisateurs.
                # self.fields["borrower_id"].queryset = User.objects.all().order_by("username")
                # Un non-staff enregistre toujours un emprunt pour lui-même.
                self.fields["borrower_id"].queryset = User.objects.filter(pk=self.user.pk)
                self.fields["borrower_id"].initial = self.user
                self.fields["borrower_id"].disabled = True
                self.fields["borrower_id"].required = False

    @staticmethod
    def _borrower_label(obj):
        name = obj.get_full_name().strip()
        return name if name else obj.username

    return_date = forms.DateField(
        label=_("Return date"),
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
    )

    class Meta:
        model = Loan
        fields = ["book", "borrower_id", "return_date", "effective_return_date"]
        labels = {
            "book": _("Book"),
            "borrower_id": _("Borrower"),
            "loan_date": _("Loan date"),
            "return_date": _("Return date"),
            "effective_return_date": _("Effective return date"),
        }
    def clean_borrower_id(self):
        borrower_id = self.cleaned_data.get("borrower_id")
        if self.user is not None and not self.user.is_staff:
            # Un non-staff emprunte toujours pour lui-même.
            return self.user
        if not borrower_id:
            raise ValidationError(_("The borrower is required."))
        return borrower_id

    def save(self, commit=True):
        if self.user is not None and not self.user.is_staff:
            # Sécurité : un non-staff ne peut jamais enregistrer un emprunt
            # pour un autre utilisateur, même en manipulant le POST.
            self.instance.borrower_id = self.user
        if self.instance.borrower_id:
            name = self.instance.borrower_id.get_full_name().strip()
            self.instance.borrower = name or self.instance.borrower_id.username
        return super().save(commit=commit)

    def clean(self):
        
        cleaned_data = super().clean()
        return_date = cleaned_data.get("return_date")
        effective_return_date = cleaned_data.get("effective_return_date")
        book = cleaned_data.get("book")

        # if book and not book.available_copies:
        #     raise ValidationError(_("This book no longer has copies available for a loan."))

        if return_date and effective_return_date and effective_return_date < return_date:
            raise ValidationError(_("The effective return date cannot be earlier than the planned return date."))

        return cleaned_data
