from django.urls import path
from . import views
urlpatterns = [

    path('all/', views.AuthorListView.as_view(), name="authors_list"),
    path('detail/<int:pk>/', views.AuthorDetailView.as_view(), name="detail_author"),
    path('create/', views.AuthorCreateView.as_view(), name="create_author"),
    path('update/<int:pk>/', views.AuthorUpdateView.as_view(), name="update_author"),
    path('delete/<int:pk>/', views.AuthorDeleteView.as_view(), name="delete_author"),
    

    
]
