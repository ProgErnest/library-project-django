from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db.models import Q


from .models import Loan
from .forms import LoanForm


# Create your views here.
## Views from Loans
class LoanCreateView(CreateView):
    model = Loan
    form_class = LoanForm
    template_name = "loan/loan_form.html"
    success_url = reverse_lazy("loan_list")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['page_title'] = _("Ajouter un auteur")
        return context

class LoanListView(ListView):
    model = Loan
    template_name = "loan/loans_list.html"
    context_object_name = "loans"
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(borrower__icontains = query) | Q(book_name__icontains = query))
        return queryset

class LoanDetailView(DetailView):
    model = Loan

class LoanUpdateView(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = "loan/loan_form.html"
    success_url = reverse_lazy("loan_list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Modifier un auteur")
        return context

class LoanDeleteView(DeleteView):
    model = Loan
    success_url = reverse_lazy("loan_list")


