from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseNotAllowed
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Author
from .forms import AuthorForm
# Create your views here.


# Sections for Autors
class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("authors_list")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['page_title'] = _("Ajouter un auteur")
        return context

class AuthorListView(ListView):
    model = Author
    template_name = "author/authors.html"
    context_object_name = "authors"

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q') or self.request.GET.get('name')
        nationality = self.request.GET.get('nationality')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(surname__icontains=query) |
                Q(biography__icontains=query)
            )

        if nationality:
            queryset = queryset.filter(nationality__icontains=nationality)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = context['authors']
        context['total_authors'] = authors.count()
        context['nationality_count'] = authors.values_list('nationality', flat=True).distinct().count()
        context['results_count'] = authors.count()
        return context

class AuthorDetailView(DetailView):
    model = Author

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("books").all() 

class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("authors_list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Modifier un auteur")
        return context

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy("authors_list")


def page_non_trouvee(request, exception):
    return render(request, "404.html", status=404)

def erreur_serveur(request):
    return render(request, "500.html", status=500)  