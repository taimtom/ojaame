from django import forms
from .models import WidrawalRequest

class WithdrawalForm(forms.ModelForm):
    
    class Meta:

        model=WidrawalRequest
        fields=(
            'ammount_request',
            
        )