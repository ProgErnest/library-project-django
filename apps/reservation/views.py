from django.shortcuts import render

# Create your views here.
# apps/reservation/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Reservation

class ReservationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservations"
    permission_required = "reservation.view_reservation"

    def get_queryset(self):
        # Chaque lecteur ne voit QUE ses propres réservations —
        # pas d'exception "bibliothécaire voit tout" ici, contrairement à Loan,
        # parce qu'une réservation est une donnée personnelle du lecteur,
        # pas une donnée de gestion de la bibliothèque.
        return Reservation.objects.filter(
            reader=self.request.user
        ).select_related("book", "book__author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservations = self.get_queryset()
        context["active_reservations_count"] = reservations.filter(is_active=True).count()
        context["active_section"] = "reservations"
        return context


class ReservationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Reservation
    fields = ["book"]
    template_name = "reservation/reservation_form.html"
    success_url = reverse_lazy("reservation_list")
    permission_required = "reservation.add_reservation"

    # def get_initial(self):
    #     initial = super().get_initial()
    #     book_pk = self.kwargs.get("book_pk")
    #     if book_pk:
    #         initial["book"] = book_pk
    #     return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nouvelle réservation"
        context["active_section"] = "reservations"
        return context

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)


class ReservationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Reservation
    template_name = "reservation/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservation_list")
    permission_required = "reservation.delete_reservation"

    def get_queryset(self):
        return Reservation.objects.filter(reader=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_section"] = "reservations"
        return context