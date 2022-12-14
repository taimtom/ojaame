from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.
from product.models import Products
from cart.models import Cart
User=settings.AUTH_USER_MODEL

class DeliveryDetails(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    company_name=models.CharField(max_length=100, null=True, blank=True)
    email=models.EmailField()
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    town=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    number=models.CharField(max_length=11)
    zip_code=models.IntegerField(null=True, blank=True)
    country_code=models.IntegerField(null=True, blank=True, default=234)
    comment=models.TextField(null=True, blank=True)

    def get_absolute_url(self):
      return reverse("delivery:delivery-info")
    

    def __str__(self):
        return self.first_name

