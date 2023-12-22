from django.db import models
#from product.models import Products
from django.conf import settings

from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator
# Create your models here.
User=settings.AUTH_USER_MODEL


COMPANY_TYPE =(
    ("W", "Wholesale Store"),
    ("M", "Manufacturer"),
)

class CompanyQuerySet(models.QuerySet):
	def search(self,query=None):
		qs=self
		if query is not None:
			look_up=(Q(name__icontains=query)|
        Q(description__icontains=query)|
        Q(product_cat__iexact=query))


			qs=qs.filter(look_up).distinct()
		return qs
    # def cat_search(self,query=None):
    #     qs=self
    #     if category_search is not None:
    #         look_up=(Q(product_cat__iexact=category_search))


    #         qs=qs.filter(look_up).distinct()
    # return qs

class CompanyManager(models.Manager):
	def get_queryset(self):
		return CompanyQuerySet(self.model, using=self._db)

	def search(self,query=None):
		return self.get_queryset().search(query)
    # def cat_search(self,query=None):
	# 	return self.get_queryset().cat_search(category_search)


class Company(models.Model):
    owner=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=11)
    company_type=models.CharField(
        max_length=1,
        choices=COMPANY_TYPE,
        default="M",
    )
    self_delivery=models.BooleanField(default=True)
    logo=models.FileField(upload_to='company/images')
    cover=models.FileField(upload_to='company/covers', null=True, blank=True)
    monitor=models.CharField(max_length=100, help_text="Ojaa monitors and enhances your mode of operation")
    average_delivery_cost=models.IntegerField(default=900)
    # areas_covered=models.CharField(max_length=260,help_text="Locations where your products can be available for delivery. Seperate each with semi colon (;)")
    description=models.TextField(null=True, blank=True)
    #products=models.ManyToManyField(Products, related_name='our_products')
    location=models.TextField()
    product_cat=models.CharField(max_length=100)
    has_paid=models.BooleanField(default=False)
    rating=models.FloatField(default=0)
    
    slug=models.SlugField(null=True, blank=True)

    objects=CompanyManager()

    def __str__(self):
        return self.name

    def get_company_url(self):
        return reverse("company:detail", kwargs={'slug':self.slug})
    def add_product_url(self):
        return reverse("company:product_add", kwargs={'slug':self.slug})

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	instance.name = instance.name.capitalize()
	if not instance.slug:
		instance.slug =unique_slug_generator(instance)
pre_save.connect(rl_pre_save_receiver, sender=Company)

def rl_post_save_receiver(sender,created, instance, *args, **kwargs):
  if created:
    cart, is_created  = Account.objects.get_or_create(company=instance)

post_save.connect(rl_post_save_receiver, sender=Company)

class Account(models.Model):
  company=models.OneToOneField(Company, on_delete=models.CASCADE)
  last_cash_recieved=models.IntegerField(default=0)
  total_income=models.IntegerField(default=0)
  available_balance=models.IntegerField(default=0)
  ledger_balance=models.IntegerField(default=0)
  
  def __str__(self):
    return self.company.name

class WidrawalRequest(models.Model):
  user=models.ForeignKey(Company, on_delete=models.CASCADE)
  ammount_request=models.CharField(max_length=240)
  date=models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.user.name

class BankAccountDetail(models.Model):
  user=models.OneToOneField(Company, on_delete=models.CASCADE)
  acc_name=models.CharField(max_length=250)
  acc_number=models.IntegerField()
  bank=models.CharField(max_length=250)
  def __str__(self):
    return self.user.owner.username