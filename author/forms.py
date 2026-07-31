from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from .models import Author

class AuthorForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Author
        fields = ['name', 'surname', 'birthday', 'nationality', 'biography']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('Le nom est obligatoire.')
        if len(name) < 2:
            raise ValidationError('Le nom doit contenir au moins 2 caractères.')
        if any(char.isdigit() for char in name):
            raise ValidationError('Le nom ne doit pas contenir de chiffres.')
        return name.title()

    def clean_surname(self):
        surname = self.cleaned_data.get('surname', '').strip()
        if not surname:
            raise ValidationError('Le prénom est obligatoire.')
        if len(surname) < 2:
            raise ValidationError('Le prénom doit contenir au moins 2 caractères.')
        if any(char.isdigit() for char in surname):
            raise ValidationError('Le prénom ne doit pas contenir de chiffres.')
        return surname.title()

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > date.today():
            raise ValidationError('La date de naissance ne peut pas être dans le futur.')
        return birthday

    def clean_nationality(self):
        nationality = self.cleaned_data.get('nationality', '').strip()
        if not nationality:
            raise ValidationError('La nationalité est obligatoire.')
        if len(nationality) < 3:
            raise ValidationError('La nationalité est trop courte.')
        return nationality.title()

    def clean_biography(self):
        biography = self.cleaned_data.get('biography', '').strip()
        if biography and len(biography) < 20:
            raise ValidationError('La biographie doit contenir au moins 20 caractères.')
        return biography

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').strip()
        surname = cleaned_data.get('surname', '').strip()

        if name and surname and name.lower() == surname.lower():
            raise ValidationError('Le nom et le prénom ne peuvent pas être identiques.')

        return cleaned_data

