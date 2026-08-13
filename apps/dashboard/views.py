from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Avg, Q
from django.utils import timezone
from apps.book.models import Book
from apps.loan.models import Loan
from apps.reservation.models import Reservation

class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    permission_required = "loan.view_all_loans"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        context.update({
            "total_books": Book.objects.count(),
            "total_active_loans": Loan.objects.filter(
                effective_return_date__isnull=True
            ).count(),
            "total_overdue": Loan.objects.filter(
                return_date__lt=today,
                effective_return_date__isnull=True
            ).count(),
            "total_active_reservations": Reservation.objects.filter(
                is_active=True
            ).count(),
            "popular_books": Book.objects.annotate(
                nb_loans=Count("loans")
            ).order_by("-nb_loans")[:5],
            "top_rated_books": Book.objects.annotate(
                avg_rating=Avg("reviews__rating"),
                nb_reviews=Count("reviews")
            ).filter(nb_reviews__gte=1).order_by("-avg_rating")[:5],
        })
        return context