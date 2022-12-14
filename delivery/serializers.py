from rest_framework import serializers
from .models import DeliveryDetails
from django.contrib.auth import get_user_model

class DeliverySerializers(serializers.ModelSerializer):
    class Meta:
        model=DeliveryDetails
        fields="__all__"

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields="__all__"