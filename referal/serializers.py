from rest_framework import serializers
from .models import Referral

from django.conf import settings
from django.contrib.auth import get_user_model
User=get_user_model()

class ReferralSerializers(serializers.ModelSerializer):
    class Meta:
        model=Referral
        fields=('id', 'user', 'customers','timestamp')
        


