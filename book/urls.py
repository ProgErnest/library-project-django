from django.urls import path
from . import views
urlpatterns = [
    path('all/', views.book_list,name="get_all_books"),
    path('detail/<int:pk>/', views.book_detail,name="book_detail"),
    path('create/', views.book_create, name="create_book"),
    path('update/<int:pk>/', views.book_update, name="update_book"),
    path('delete/<int:pk>/', views.book_delete, name="delete_book"),

]
