from django import forms

from .models import Company, BankAccountDetail
from product.models import Products
CATEGORY_CHOICES =( ("fashion", "Fashion"), ("electronics and phones", "Electronics & Phones"), ("home and kitchen", "Home & Kitchen"), ("furnitures and woodworks", "Furnitures & Woodworks"), ("pets and livestocks", "Pets & Livestocks"), ("health and beauty", "Health & Beauty"),("automobiles and industrial machines", "Automobiles & Industrial Machines")) 
 

    
class CompanyForm(forms.ModelForm):
    product_cat = forms.ChoiceField(choices = CATEGORY_CHOICES) 

    class Meta:
        model=Company
        
        fields=(
            'name',
            'email',
            'phone',
            'company_type',
            'product_cat',
            'description',
            'location',
            # "areas_covered",
            # "average_delivery_cost",
            'logo',
            'cover',
        )
            
            

        labels = {
        "product_cat": "Product Category"
        }        
        widgets={
            'name':forms.TextInput(attrs={'placeholder':'Company Name'}),
            'email':forms.EmailInput(attrs={'placeholder':'Email Account'}),
            'phone':forms.TextInput(attrs={'placeholder':'Phone Number'}),
            'email':forms.TextInput(attrs={'placeholder':'Email Name'}),
            'description':forms.TextInput(attrs={'placeholder':'Description of Company'}),
            'location':forms.TextInput(attrs={'placeholder':'Address of Company'}),
            'logo':forms.ClearableFileInput(attrs={'placeholder':'Logo of company'}),
            'product_cat':forms.TextInput(attrs={'placeholder':'Product Category'}),
            
        }
class CompanyAccountForm(forms.ModelForm):
    
    class Meta:
        model=BankAccountDetail
        fields=(
            "acc_name",
            "acc_number",
            "bank"

        )
        labels = {
        "acc_name": "Account Name",
        "acc_number": "Account Number",
        "bank": "Bank"

        }
        widgets={
            'acc_name':forms.TextInput(attrs={'placeholder':'Account Holder`s Name'}),
            'acc_number':forms.TextInput(attrs={'placeholder':'Account Number'}),
            'bank':forms.TextInput(attrs={'placeholder':'Bank Name'}),
        }   
# class ProductForm(forms.ModelForm):
    
#     class Meta:
#         model=Products
#         fields=(
#             'name',
#             'category',
#             'sub_category',
#             'price',
#             'discounted_from',
#             'availability',
#             'brand',
#             'size',
#             'description',
#             'color',
#             'image',
#         )
       