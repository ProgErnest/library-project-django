from django.contrib import admin
from.models import Loan
# Register your models here
class LoanAdmin(admin.ModelAdmin):
    list_filter = ('loan_date',)
    search_field = ('borrower','book.title')
    readonly_fields = ('loan_date','id')

admin.site.register(Loan, LoanAdmin)
