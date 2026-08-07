    
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.db.models import Q,F, Avg, Count
from django.urls import reverse_lazy
from .models import Book, Genre
from .forms import CreateBookForm, GenreForm


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add a book")
        return context


class BookListView(ListView):
    model = Book
    template_name = "book/book_list.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.select_related(
            "author", "genre_id"
        ).annotate(
            note_moyenne=Avg("reviews__rating"),
            nb_emprunts=Count("loans"),
            available_copies=F("total_copies") - F("unavailable_copies"),
        )
        query = self.request.GET.get("q")
        genre = self.request.GET.get("genre_id")
        availability = self.request.GET.get("available")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(subtitle__icontains=query) | Q(summary__icontains=query)
            )

        if genre:
            queryset = queryset.filter(Q(genre_id=genre))

        if availability:
            if availability == "0":
                queryset = queryset.filter(Q(unavailable_copies__gte=F("total_copies")))
            else:
                queryset = queryset.filter(Q(unavailable_copies__lt=F("total_copies")))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        total = books.values_list("total_copies", flat=True)
        context["total_books"] = books.count()
        context["available_books"] = books.filter(unavailable_copies__lt=F("total_copies")).count()
        context["unavailable_books"] = books.filter(unavailable_copies__gte=F("total_copies"), total_copies__gt=F("unavailable_copies")).count()
        context["availability_rate"] = round((context["available_books"] / context["total_books"]) * 100, 1) if context["total_books"] else 0
        context["genres"] = Genre.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "book/book_detail.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("author", "genre_id").prefetch_related("reviews","loans__borrower_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context["available_copies"] = book.total_copies - book.unavailable_copies
        context["percent"] = ((book.total_copies - book.unavailable_copies) / book.total_copies) * 100 if book.total_copies else 0
        context["reviews"] = book.reviews.select_related("reviewer").all()
        context["average_rating"] = book.reviews.aggregate(Avg("rating"))["rating__avg"]
        context["total_loans"] = book.loans.count()
        context["can_borrow"] = (
            self.request.user.is_authenticated and self.object.total_copies - self.object.unavailable_copies > 0
        )
        return context


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit a book")
        return context


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = "book.delete_book"
    success_url = reverse_lazy("get_all_books")
    raise_exception = True

#__________________________Genre Views__________________________


class GenreListView(ListView):
    model = Genre
    template_name = "book/genre_list.html"
    context_object_name = "genres"
    def get_queryset(self):
        return super().get_queryset().annotate(nb_books=Count("books")).order_by("name")

class GenreDetailView(DetailView):
    model = Genre
    template_name = "book/genre_detail.html"
    context_object_name = "genre"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("books")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = self.get_object()
        context["books"] = genre.books.select_related("author").annotate(
            note_moyenne = Avg("reviews__rating"),
            nb_emprunts = Count("loans")
        )
        return context

class GenreCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = "book/genre_form.html"
    success_url = reverse_lazy("get_all_genres")
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add a genre")
        return context