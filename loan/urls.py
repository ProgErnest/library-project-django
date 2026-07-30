from django.urls import path
from . import views
urlpatterns = [
    path('all/', views.LoanListView.as_view(), name="loan_list"),
    path('detail/<int:pk>/', views.LoanDetailView.as_view(), name="detail_loan"),
    path('create/', views.LoanCreateView.as_view(), name="initiate_loan"),
    path('update/<int:pk>/', views.LoanUpdateView.as_view(), name="update_loan"),
    path('delete/<int:pk>/', views.LoanDeleteView.as_view(), name="delete_loan"),   
]

