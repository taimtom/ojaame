from django.contrib import admin

# Register your models here.
from .models import SaleRecord,Pack

admin.site.register(SaleRecord)
admin.site.register(Pack)