from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from product.models import Products
from accounts.models import SaleRecord

User=settings.AUTH_USER_MODEL


# Create your models here.
class CartManager(models.Manager):
	def toggle_product(self,sale_record, user_to_toggle):
		cart_=Cart.objects.get(user=user_to_toggle)
		product=sale_record
		in_cart=False
		if product in cart_.content.all():
			cart_.content.remove(product)
			product.delete()
			

		else:
			cart_.content.add(product)

			
			
			in_cart=True
		return cart_,in_cart

class Cart(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	content=models.ManyToManyField(SaleRecord, related_name='in_cart', blank=True)
	total=models.IntegerField( default=0)
	delivery_type=models.CharField(max_length=100, default="regular")
	advert_email_unsubscribe=models.BooleanField(default=False)
	

	objects=CartManager()


	def __str__(self):
		return self.user.username
	
	def total_price(self):
		total_price=0
		for sale in self.content.all():
			total_price =+ sale.price
		return total_price
	
	


def post_save_user_receiver(sender,instance,created,*args, **kwargs):


	if created:
		cart, is_created  = Cart.objects.get_or_create(user=instance)


post_save.connect(post_save_user_receiver, sender=User)

