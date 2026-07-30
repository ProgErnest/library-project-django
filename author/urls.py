from django.urls import path
from . import views
urlpatterns = [

    path('all/', views.list_authors, name="authors_list"),
    path('detail/<int:pk>/', views.detail_author, name="detail_author"),
    path('create/', views.create_author, name="create_author"),
    path('update/<int:pk>/', views.update_author, name="update_author"),
    path('delete/<int:pk>/', views.delete_author, name="delete_author"),
    

    
]
