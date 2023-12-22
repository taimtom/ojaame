from django import forms
from .models import Products
CATEGORY_CHOICES =( ("New", "New Product"), ("Used", "Fairly Used Product")) 
class ProductForm(forms.ModelForm):

    # # creating a form  
    status = forms.ChoiceField(choices = CATEGORY_CHOICES) 
    class Meta:

        model=Products
        fields=(
            'name',
            'price',
            'discounted_from',
            'availability',
            "status",
            'brand',
            'size',
            'description',
            'color',
            'image',
        )
        widgets={
            'name':forms.TextInput(attrs={'placeholder':'Product Name'}),
            # 'category':forms.ChoiceField(choices = CATEGORY_CHOICES),
            # 'sub_category':forms.TextInput(attrs={'placeholder':'Sub Category'}),
            'price':forms.TextInput(attrs={'placeholder':'Price'}),
            'discounted_from':forms.TextInput(attrs={'placeholder':'Former Price'}),
            'availability':forms.TextInput(attrs={'placeholder':'Availability'}),
            'brand':forms.TextInput(attrs={'placeholder':'Brand'}),
            'size':forms.TextInput(attrs={'placeholder':'Size e.g S, M, L, 41,42 ...'}),
            'color':forms.TextInput(attrs={'placeholder':'Color'}),
        }


    