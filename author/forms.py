from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    birthday = forms.DateField(
        widget= forms.DateInput(attrs = {'type': 'date'})
    )
    class Meta:
        model = Author
        fields = ['name','surname','birthday', 'nationality', 'biography']

