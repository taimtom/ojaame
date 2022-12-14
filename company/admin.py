from django.contrib import admin

# Register your models here.
from .models import Company, Account,BankAccountDetail,WidrawalRequest

admin.site.register(Company)
admin.site.register(Account)
admin.site.register(BankAccountDetail)
admin.site.register(WidrawalRequest)