from django.contrib import admin
from .models import Book
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'isbn', 'language', 'genre', 'num_pages', 'publication_date', 'available', 'author', 'summary', 'total_copies', 'available_copies')
    search_fields = ('title', 'subtitle', 'isbn', 'author__name', 'author__surname')
    
admin.site.register(Book)