from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Author


class AuthorForm(forms.ModelForm):
    birthday = forms.DateField(
        label=_("Birthday"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Author
        fields = ["name", "surname", "birthday", "nationality", "biography"]
        labels = {
            "name": _("Name"),
            "surname": _("Surname"),
            "birthday": _("Birthday"),
            "nationality": _("Nationality"),
            "biography": _("Biography"),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise ValidationError(_("The name is required."))
        if len(name) < 2:
            raise ValidationError(_("The name must contain at least 2 characters."))
        if any(char.isdigit() for char in name):
            raise ValidationError(_("The name must not contain digits."))
        return name.title()

    def clean_surname(self):
        surname = self.cleaned_data.get("surname", "").strip()
        if not surname:
            raise ValidationError(_("The surname is required."))
        if len(surname) < 2:
            raise ValidationError(_("The surname must contain at least 2 characters."))
        if any(char.isdigit() for char in surname):
            raise ValidationError(_("The surname must not contain digits."))
        return surname.title()

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday and birthday > date.today():
            raise ValidationError(_("The birth date cannot be in the future."))
        return birthday

    def clean_nationality(self):
        nationality = self.cleaned_data.get("nationality", "").strip()
        if not nationality:
            raise ValidationError(_("The nationality is required."))
        if len(nationality) < 3:
            raise ValidationError(_("The nationality is too short."))
        return nationality.title()

    def clean_biography(self):
        biography = self.cleaned_data.get("biography", "").strip()
        if biography and len(biography) < 20:
            raise ValidationError(_("The biography must contain at least 20 characters."))
        return biography

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name", "").strip()
        surname = cleaned_data.get("surname", "").strip()

        if name and surname and name.lower() == surname.lower():
            raise ValidationError(_("The name and the surname cannot be identical."))

        return cleaned_data

