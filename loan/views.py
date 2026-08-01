from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.utils import timezone
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
        context['page_title'] = _("Ajouter un emprunt")
        return context

class LoanListView(ListView):
    model = Loan
    template_name = "loan/loans_list.html"
    context_object_name = "loans"

    def get_queryset(self):
        queryset = super().get_queryset().select_related('book')

        query = self.request.GET.get('q') or self.request.GET.get('borrower')
        status = self.request.GET.get('status')

        if query:
            queryset = queryset.filter(
                Q(borrower__icontains=query) |
                Q(book__title__icontains=query)
            )

        if status:
            today = timezone.now().date()
            if status == "En cours":
                queryset = queryset.filter(effective_return_date__isnull=True, return_date__gte=today)
            elif status == "En retard":
                queryset = queryset.filter(effective_return_date__isnull=True, return_date__lt=today)
            elif status == "Rendu":
                queryset = queryset.filter(effective_return_date__isnull=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loans = context['loans']
        context['total_loans'] = loans.count()
        context['results_count'] = loans.count()
        return context

class LoanDetailView(DetailView):
    model = Loan

class LoanUpdateView(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = "loan/loan_form.html"
    success_url = reverse_lazy("loan_list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Modifier un emprunt")
        return context

class LoanDeleteView(DeleteView):
    model = Loan
    success_url = reverse_lazy("loan_list")


