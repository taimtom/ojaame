from django.db import models
from product.models import Products
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from .utils import unique_pkg_generator
User=settings.AUTH_USER_MODEL

# Create your models here.
class SaleRecord(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  product=models.ForeignKey(Products, on_delete=models.CASCADE)
  color=models.CharField(max_length=20, null=True, blank=True)
  size=models.CharField(max_length=20, null=True, blank=True)
  status=models.CharField(max_length=20, null=True, blank=True)
  package_number=models.CharField(max_length=20, null=True, blank=True)
  paid=models.BooleanField(default=False)
  returned_time=models.DateTimeField(null=True,blank=True)
  delivery_time=models.DateTimeField(null=True,blank=True)
  package_time=models.DateTimeField(null=True,blank=True)
  collected_time=models.DateTimeField(null=True,blank=True, help_text='Date item was collected by delivery company')
  quantity=models.IntegerField(default=1)
  price_per_one=models.DecimalField(max_digits=20, decimal_places=2)
  shiping_msg=models.CharField(max_length=250, null=True, blank=True)
  price=models.DecimalField(max_digits=20, decimal_places=2)
  timestamp=models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering=["-timestamp"]
  def __str__(self):
    return self.product.name

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.package_number:
		instance.package_number =unique_pkg_generator(instance)
pre_save.connect(rl_pre_save_receiver, sender=SaleRecord)
  
  
  
class Pack(models.Model):
  user= models.ForeignKey(User, on_delete=models.CASCADE)
  contents=models.ManyToManyField(SaleRecord, blank=True)
  timestamp=models.DateTimeField(auto_now_add=True)
  date_delivered=models.DateTimeField(null=True,blank=True)
  total_price=models.IntegerField(default=0)
  delivery_fee=models.IntegerField(default=0)
  delivery_type=models.CharField(max_length=100, default="regular")
  class Meta:
    ordering=["-timestamp"]
  
  def __str__(self):
    return self.user.username

