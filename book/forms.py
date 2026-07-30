from django import forms
from .models import Book

class CreateBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title','subtitle','language','genre','isbn','author','num_pages','available','publication_date','total_copies','summary']
        localized_fields = ['publication_date']
        widgets= {
            'title': forms.TextInput(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : Le Petit Prince'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : Le livre de la royaute'
            }),
            'language': forms.TextInput(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : French'
            }),
            'genre': forms.TextInput(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : Roman'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : 978-3-16-148410-0'
            }),
            'num_pages': forms.TextInput(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : 978-3-16-148410-0'
            }),
            'total_copies': forms.TextInput(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : 978-3-16-148410-0'
            }),
            'author': forms.Select(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 accent-indigo-500 rounded cursor-pointer shrink-0',
                'checked': False
            }),
            'publication_date': forms.DateInput(
                attrs={
                'type': 'date',
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-700 bg-slate-50 border border-slate-200 rounded-lg shadow-xs outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100'
                }
            ),
            'summary': forms.Textarea(attrs={
                'class': 'w-full pl-9 pr-4 py-2.5 text-sm text-slate-800 bg-slate-50 border border-slate-200 rounded-lg shadow-xs placeholder:text-slate-400 placeholder:italic outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-3 focus:ring-indigo-100',
                'placeholder': 'Ex : 978-3-16-148410-0'
            }),
        }
    
