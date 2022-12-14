from django import forms
from .models import SaleRecord

class SaleRecordForm(forms.ModelForm):
    
    class Meta:

        model=SaleRecord
        fields=(
            "product",
            "user",
            "price"

        )

