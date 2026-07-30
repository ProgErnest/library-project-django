from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseNotAllowed
from django.utils.translation import gettext as _

from .models import Author
from .forms import AuthorForm
# Create your views here.


# Sections for Autors

def list_authors(request):
    if request.GET.get('q') != None:
        search = request.GET.get('q')
        authors = Author.objects.filter(name__icontains = search)
    else:
        authors = Author.objects.all()
    return render(request, "author/authors.html", {"authors" : authors})

def detail_author(request,pk):
    author = get_object_or_404(Author, id = pk)
    books = author.book_set.all()
    return render(request,"author/detail_author.html",{"author": author, "books": books})

def create_author(request):
    if (request.method == "POST"):
        author_form = AuthorForm(request.POST)
        if(author_form.is_valid()):
            author_form.save()
            return redirect("authors_list")
    else:
        author_form = AuthorForm()
    return render(request,"author/author_form.html",{"author_form": author_form})
def update_author(request, pk):
    author = get_object_or_404(Author, id=pk)
    if (request.method == "POST"):
        author_form = AuthorForm(request.POST, instance=author)
        if(author_form.is_valid()):
            author_form.save()
            return redirect("authors_list")
    else:
        author_form = AuthorForm(instance=author)
    return render(request,"author/author_form.html",{"author_form": author_form})
    
def delete_author(request,pk):
    if(request.method == "POST"):
        author = get_object_or_404(Author, id=pk)
        author.delete()
        return redirect("authors_list")
    return HttpResponseNotAllowed(['POST'])
    


def page_non_trouvee(request, exception):
    return render(request, "404.html", status=404)

def erreur_serveur(request):
    return render(request, "500.html", status=500)  