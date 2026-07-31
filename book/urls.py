from django.urls import path
from . import views
urlpatterns = [
    path('all/', views.BookListView.as_view(),name="get_all_books"),
    path('detail/<int:pk>/', views.BookDetailView.as_view(),name="book_detail"),
    path('create/', views.BookCreateView.as_view(), name="create_book"),
    path('update/<int:pk>/', views.BookUpdateView.as_view(), name="update_book"),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name="delete_book"),

]
