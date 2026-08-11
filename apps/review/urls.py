from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path("books/<int:book_pk>/reviews/create/", views.ReviewCreateView.as_view(), name="create_review"),
    path("reviews/<int:pk>/update/", views.ReviewUpdateView.as_view(), name="update_review"),
    path("reviews/<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="delete_review"),
]
