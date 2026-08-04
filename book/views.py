from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.db.models import Q,F
from django.urls import reverse_lazy

from .models import Book
from .forms import CreateBookForm


class BookCreateView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add a book")
        return context


class BookListView(ListView):
    model = Book
    template_name = "book/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        genre = self.request.GET.get("genre")
        availability = self.request.GET.get("available")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(subtitle__icontains=query) | Q(summary__icontains=query)
            )

        if genre:
            queryset = queryset.filter(Q(genre=genre))

        if availability:
            if availability == "0":
                queryset = queryset.filter(Q(unavailable_copies__gte=total_copies))
            else:
                queryset = queryset.filter(Q(unavailable_copies__lt=total_copies))

        return queryset.select_related("author").annotate(available_copies=F("total_copies") - F("unavailable_copies"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        total = books.values_list("total_copies", flat=True)
        context["total_books"] = books.count()
        context["available_books"] = books.filter(unavailable_copies__lt=total).count()
        context["unavailable_books"] = books.filter(unavailable_copies__gte=total).count()
        context["availability_rate"] = round((context["available_books"] / context["total_books"]) * 100, 1) if context["total_books"] else 0
        context["genres"] = books.values_list("genre", flat=True).distinct()
        return context


class BookDetailView(DetailView):
    model = Book

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context["available_copies"] = book.total_copies - book.unavailable_copies
        context["percent"] = ((book.total_copies - book.unavailable_copies) / book.total_copies) * 100 if book.total_copies else 0
        return context


class BookUpdateView(UpdateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit a book")
        return context


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy("get_all_books")
