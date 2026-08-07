from django.contrib import admin
from .models import Book, Genre
# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Genre, GenreAdmin)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'isbn', 'language', 'genre_id', 'num_pages', 'publication_date', 'author', 'total_copies', 'unavailable_copies')
    search_fields = ('title', 'subtitle', 'isbn', 'author__name', 'author__surname')
    list_filter = ('genre_id', 'language', 'publication_date', 'author')
    list_select_related = ('author', 'genre_id')
    
# admin.site.register(Book, BookAdmin)