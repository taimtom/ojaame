from rest_framework import serializers
from reviews.models import Review
from .models import Products

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=('id', 'rating', 'content', 'user','timestamp')

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields="__all__"