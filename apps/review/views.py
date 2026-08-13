from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from apps.book.models import Book
from .models import Review
from .forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review/review_form.html"
    permission_required = "review.add_review"

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs["book_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.book = self.book
        form.instance.reviewer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.book.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add a review")
        context["book"] = self.book
        return context


class ReviewUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review/review_form.html"
    permission_required = "review.change_review"

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def get_success_url(self):
        return self.object.book.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit a review")
        context["book"] = self.object.book
        return context


class ReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = "review/review_confirm_delete.html"
    permission_required = "review.delete_review"
    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def get_success_url(self):
        return self.object.book.get_absolute_url()