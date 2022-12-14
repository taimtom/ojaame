from rest_framework import serializers
from .models import SaleRecord,Pack

class SaleRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=SaleRecord
        fields=('id','user', 'product', 'quantity','price')
class PackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pack
        fields=('id', 'contents', 'total_price', 'user')