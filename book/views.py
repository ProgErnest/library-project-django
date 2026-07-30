from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils.translation import gettext as _
from .models import Book
from .forms import CreateBookForm

# Create your views here.
def book_list(request):
    if request.GET.get('q') != None: 
        search = request.GET.get('q')
        books = Book.objects.filter(title__icontains = search)
    else:
        books = Book.objects.all()
    return render(request, "book/book_list.html", {'books':books})   

def book_detail(request, pk):
    book = get_object_or_404(Book, id = pk)
    return render(request,"book/book_detail.html", {'book' : book})

def book_create(request):
    if (request.method == "POST"):
        form = CreateBookForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect("get_all_books")

    elif (request.method == "GET"):
        page_title = _("Ajouter un livre")
        form = CreateBookForm()
        return render(request,"book/create_form.html", {
            "form": form,
            "page_title": page_title,
            })

    return HttpResponseNotAllowed(['POST','GET'])

def book_update(request, pk):
    book = get_object_or_404(Book,id=pk)
    page_title = _("Modifier un livre")
    if (request.method == "POST"):
        form = CreateBookForm(request.POST, instance = book)
        if(form.is_valid()):
            form.save()
            return redirect("get_all_books")
    else:
        form = CreateBookForm(instance = book)
    return render(request,"book/create_form.html", {
        "form": form,
        "page_title": page_title,
        })



def book_delete(request,pk):
    if request.method == 'POST':
        book = get_object_or_404(Book,id=pk)
        book.delete()
        return redirect("get_all_books")
    return HttpResponseNotAllowed(['POST'])
            
