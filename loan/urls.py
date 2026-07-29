from django.urls import path
from . import views
urlpatterns = [
    path('all/', views.list_loans, name="loan_list"),
    path('detail/<int:pk>/', views.detail_loan, name="detail_loan"),
    path('create/', views.initiate_loan, name="initiate_loan"),
    path('update/<int:pk>/', views.update_loan, name="update_loan"),
    path('delete/<int:pk>/', views.delete_loan, name="delete_loan"),   
]

