# apps/reservation/urls.py
from django.urls import path
from . import views

# app_name = "reservation"

urlpatterns = [
    path("", views.ReservationListView.as_view(), name="reservation_list"),
    path("create/<int:book_pk>/", views.ReservationCreateView.as_view(), name="reservation_create"),
    path("<int:pk>/delete/", views.ReservationDeleteView.as_view(), name="reservation_delete"),
]