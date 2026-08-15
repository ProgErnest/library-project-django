    
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.db.models import Q,F, Avg, Count
from django.urls import reverse_lazy
from django.core.cache import  cache
from .models import Book, Genre
from .forms import CreateBookForm, GenreForm
from django.shortcuts import get_object_or_404

class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")
    raise_exception = True
    permission_required = "book.add_book"

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
        ).only(
            "id",
            "isbn",
            "num_pages",
            "publication_date",
            "title",
            "subtitle",
            "author__name",
            "author__surname",
            "language",
            "genre_id",
            "total_copies",
            "unavailable_copies",
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
        book = get_object_or_404(Book, id=self.kwargs["pk"])
        context["available_copies"] = book.total_copies - book.unavailable_copies
        context["percent"] = ((book.total_copies - book.unavailable_copies) / book.total_copies) * 100 if book.total_copies else 0
        context["reviews"] = book.reviews.select_related("reviewer").order_by("-date")
        context["average_rating"] = book.reviews.aggregate(Avg("rating")).get("rating__avg")
        context["total_loans"] = book.loans.count()
        context["rating_range"] = range(1, 6)
        context["can_borrow"] = (
            self.request.user.is_authenticated and self.object.total_copies - self.object.unavailable_copies > 0
        )

        reviews_qs = book.reviews.all()
        total_reviews = reviews_qs.count()
        distribution_brute = (
            book.reviews.values("rating")
            .annotate(count=Count("id"))
            .order_by("rating")
        )
        comptes = {item["rating"]: item["count"] for item in distribution_brute}

        context["total_reviews"] = total_reviews
        context["rating_distribution"] = {
            star: {
                "count": comptes.get(star, 0),
                "percent": round((comptes.get(star, 0) / total_reviews) * 100, 1) if total_reviews else 0,
            }
            for star in range(5, 0, -1)
        }
        return context


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = CreateBookForm
    template_name = "book/create_form.html"
    success_url = reverse_lazy("get_all_books")
    raise_exception = True
    permission_required = "book.change_book"
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
        queryset = cache.get("list_genres")
        if not queryset:
            queryset = super().get_queryset().prefetch_related("books").annotate(nb_books=Count("books")).order_by("name")
            cache.set("list_genres", queryset, 60)
        return queryset


class GenreDetailView(DetailView):
    model = Genre
    template_name = "book/genre_detail.html"
    context_object_name = "genre"

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = context["genre"]
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
    permission_required = "book.add_genre"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add a genre")
        return context