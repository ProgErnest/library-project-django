from django.urls import path
from . import views
urlpatterns = [
    # Books
    path('', views.BookListView.as_view(),name="get_all_books"),
    path('<int:pk>/', views.BookDetailView.as_view(),name="book_detail"),
    path('create/', views.BookCreateView.as_view(), name="create_book"),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name="update_book"),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name="delete_book"),

    # Genres
    path('genres/', views.GenreListView.as_view(), name="get_all_genres"),
    path('genres/<slug:slug>/', views.GenreDetailView.as_view(), name="genre_detail"),
    path('genres/create/', views.GenreCreateView.as_view(), name="create_genre")
]
