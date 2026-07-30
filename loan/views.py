from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _

from .models import Loan
from .forms import LoanForm


# Create your views here.
## Views from Loans

def list_loans(request):
    loans = Loan.objects.all()
    return render(request, "loan/loans_list.html",{"loans": loans})

def detail_loan(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    return render(request, "loan/loan_detail.html", {"loan":loan})

def initiate_loan(request):
    loan_form = LoanForm(request.POST or None)
    if(request.method == "POST"):
        if loan_form.is_valid():
            book = loan_form.cleaned_data['book']
            book.available = False
            book.save()
            loan_form.save()
            return redirect("loan_list")
    return render(request, "loan/loan_form.html", {"loan_form": loan_form})

def update_loan(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    loan_form = LoanForm(request.POST or None, instance=loan)
    if(request.method == "POST"):
        if loan_form.is_valid():
            loan_form.save()
            return redirect("loan_list")
    return render(request, "loan/loan_form.html", {"loan_form": loan_form})
    

@require_POST
def delete_loan(request,pk):
    loan = get_object_or_404(Loan, id=pk)
    loan.delete()
    return redirect("loan_list")

