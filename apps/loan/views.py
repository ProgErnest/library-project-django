from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Loan
from .forms import LoanForm


class LoanCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Loan
    form_class = LoanForm
    template_name = "loan/loan_form.html"
    success_url = reverse_lazy("loan_list")
    permission_required = "loan.add_loan"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add a loan")
        context["is_staff"] = self.request.user.is_staff
        return context
    def form_valid(self, form):
        return super().form_valid(form)

class LoanListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Loan
    template_name = "loan/loans_list.html"
    context_object_name = "loans"
    paginate_by = 20
    permission_required = "loan.view_loan"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("book", "book__author", "book__genre_id", "borrower_id")

        query = self.request.GET.get("q") or self.request.GET.get("borrower")
        status = self.request.GET.get("status")

        if query:
            queryset = queryset.filter(Q(borrower__icontains=query) | Q(book__title__icontains=query))

        if status:
            today = timezone.now().date()
            if status == _("In progress"):
                queryset = queryset.filter(effective_return_date__isnull=True, return_date__gte=today)
            elif status == _("Late"):
                queryset = queryset.filter(effective_return_date__isnull=True, return_date__lt=today)
            elif status == _("Returned"):
                queryset = queryset.filter(effective_return_date__isnull=False)
        if self.request.user.is_authenticated and self.request.user.has_perm("loan.view_all_loans"):
            return queryset
        return queryset.filter(borrower=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loans = context["loans"]
        context["total_loans"] = loans.count()
        context["results_count"] = loans.count()
        return context


class LoanDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Loan
    permission_required = "loan.view_loan"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("book", "book__author", "book__genre_id", "borrower_id")
        if self.request.user.is_authenticated and self.request.user.has_perm("loan.view_all_loans"):
            return queryset
        return queryset.filter(borrower=self.request.user)

class LoanUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = "loan/loan_form.html"
    success_url = reverse_lazy("loan_list")
    permission_required = "loan.change_loan"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit a loan")
        context["is_staff"] = self.request.user.is_staff
        return context


class LoanDeleteView(DeleteView, PermissionRequiredMixin):
    model = Loan
    success_url = reverse_lazy("loan_list")
    permission_required = "loan.delete_loan"

