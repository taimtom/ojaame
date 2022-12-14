from django import forms
from .models import DeliveryDetails

class CheckoutForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    class Meta:

        model=DeliveryDetails
        fields=(
            'first_name',
            'last_name',
            'email',
            'country',
            'state',
            'town',
            'street',
            'number',
            'comment',

        )
        widgets={
            'first_name':forms.TextInput(attrs={'placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last Name'}),
            'email':forms.TextInput(attrs={'placeholder':'Email Name'}),
            'country':forms.TextInput(attrs={'placeholder':'Country Name'}),
            'state':forms.TextInput(attrs={'placeholder':'State Name'}),
            'town':forms.TextInput(attrs={'placeholder':'Town Name'}),
            'street':forms.TextInput(attrs={'placeholder':'Street '}),
            'number':forms.TextInput(attrs={'placeholder':'Phone Number'}),
            'comment':forms.TextInput(attrs={'placeholder':'Comment (optional)'}),
        }


    