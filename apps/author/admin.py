from django.contrib import admin
from .models import Author
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'birthday', 'nationality')
    search_fields = ('name', 'surname')
    list_filter = ('nationality', 'birthday')
    ordering = ('name', 'surname')
    list_per_page = 10

admin.site.register(Author, AuthorAdmin)
