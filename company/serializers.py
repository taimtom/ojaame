from rest_framework import serializers
from .models import Company

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields="__all__"

# class ProductSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Products
#         fields="__all__"