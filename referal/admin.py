from django.contrib import admin

# Register your models here.
from .models import Referral,WidrawalRequest,BankAccountDetail,Account

admin.site.register(Referral)
admin.site.register(Account)
admin.site.register(BankAccountDetail)
admin.site.register(WidrawalRequest)