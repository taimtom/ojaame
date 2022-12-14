from rest_framework import serializers
from .models import Wish


class WishSerializers(serializers.ModelSerializer):
    class Meta:
        model=Wish
        fields="__all__"