# apps/review/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "hidden"}),
            "comment": forms.Textarea(attrs={"class": "w-full rounded-lg border border-gray-300 px-3 py-2", "rows": 4}),
        }