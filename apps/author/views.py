from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Author
from .forms import AuthorForm


class AuthorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("authors_list")
    permission_required = "author.add_author"
    raise_exception =  True
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add an author")
        return context


class AuthorListView(ListView):
    model = Author
    template_name = "author/authors.html"
    context_object_name = "authors"

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get("q") or self.request.GET.get("name")
        nationality = self.request.GET.get("nationality")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(surname__icontains=query)
                | Q(biography__icontains=query)
            )

        if nationality:
            queryset = queryset.filter(nationality__icontains=nationality)

        return queryset.prefetch_related('books').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = context["authors"]
        author_list = Author.objects.all()
        context["total_authors"] = author_list.count()
        context["nationality_count"] = author_list.values_list("nationality", flat=True).distinct().count()
        context["nationalities"] = author_list.values_list("nationality", flat=True).distinct()
        context["results_count"] = authors.count()
        return context


class AuthorDetailView(DetailView):
    model = Author

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("books").all()


class AuthorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("authors_list")
    permission_required = "author.change_author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit an author")
        return context


class AuthorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authors_list")


def page_non_trouvee(request, exception):
    return render(request, "errors/404.html", status=404)


def erreur_serveur(request):
    return render(request, "errors/500.html", status=500)