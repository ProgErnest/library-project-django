from django.shortcuts import render

# Create your views here.
# apps/reservation/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Reservation

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        # Chaque lecteur ne voit QUE ses propres réservations —
        # pas d'exception "bibliothécaire voit tout" ici, contrairement à Loan,
        # parce qu'une réservation est une donnée personnelle du lecteur,
        # pas une donnée de gestion de la bibliothèque.
        return Reservation.objects.filter(
            reader=self.request.user
        ).select_related("book", "book__author")


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ["book"]
    template_name = "reservation/reservation_form.html"
    success_url = reverse_lazy("reservation_list")

    def form_valid(self, form):
        form.instance.reader = self.request.user  # auto-assigné, jamais choisi par l'utilisateur
        return super().form_valid(form)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = "reservation/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservation_list")

    def get_queryset(self):
        # Protection IDOR : impossible de supprimer la réservation d'un autre
        return Reservation.objects.filter(reader=self.request.user)