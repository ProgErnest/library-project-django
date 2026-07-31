from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils.translation import gettext as _
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView 
from django.db.models import Q
from django.urls import reverse_lazy

from .models import Book
from .forms import CreateBookForm

# Create your views here.
class BookCreateView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['page_title'] = _("Ajouter un livre")
        return context

class BookListView(ListView):
    model = Book
    template_name = "book/book_list.html"
    context_object_name = "books"
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains = query) | Q(subtitle__icontains = query) | Q(summary__icontains = query))
        return queryset.select_related('author')
 
class BookDetailView(DetailView):
    model = Book
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['percent'] = (book.available_copies/book.total_copies)*100
        return context

class BookUpdateView(UpdateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Modifier un livre")
        return context



class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy("get_all_books")
