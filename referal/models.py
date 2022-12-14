from django.db import models
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save, post_save


User=settings.AUTH_USER_MODEL
# Create your models here.
class ReferrerManager(models.Manager):
  def toggle_customer(self,request_customer,referral_link):
    referrer=Referral.objects.get(referral_link__iexact=referral_link)
    in_customer=False
    
    if request_customer not in referrer.customers.all():
      referrer.customers.add(request_customer)
      in_customer=True
      referred_by=referrer
      referred_by.account.units=referred_by.account.units+1
      if referred_by.account.units >= 10 and referred_by.account.percent_commition < 85:
          referred_by.account.percent_commition=referred_by.account.percent_commition+1
          referred_by.account.units=0
      referred_by.account.save()
    return referrer,in_customer

class Referral(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    referral_link=models.CharField(max_length=250)
    customers=models.ManyToManyField(User, related_name='is_customer')
    mygain=models.IntegerField(null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    objects=ReferrerManager()

    def __str__(self):
      return self.user.username

    def get_absolute_url(self):
      return reverse("referral:detail", kwargs={'username':self.user.username})
    
    def get_link_url(self):
      return reverse("referral:register", kwargs={'referral_link':self.referral_link})
class Account(models.Model):
  referrer=models.OneToOneField(Referral, on_delete=models.CASCADE)
  last_commistion_recieved=models.IntegerField(default=0)
  total_commition=models.IntegerField(default=0)
  percent_commition=models.CharField(max_length=20,default=50)
  ledger_balance=models.IntegerField(default=0)
  units=models.IntegerField(default=0)
  available_balance=models.IntegerField(default=0)
  def __str__(self):
    return self.referrer.user.username

class WidrawalRequest(models.Model):
  user=models.ForeignKey(Referral, on_delete=models.CASCADE)
  ammount_request=models.CharField(max_length=240)
  date=models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.user.user.username

class BankAccountDetail(models.Model):
  user=models.ForeignKey(Referral, on_delete=models.CASCADE)
  acc_name=models.CharField(max_length=250)
  acc_number=models.IntegerField()
  bank=models.CharField(max_length=250)

  def __str__(self):
    return self.acc_name


def post_save_user_receiver(sender,instance,created,*args, **kwargs):


	if created:
		account, is_created  = Account.objects.get_or_create(referrer=instance,available_balance=3500)
   

		# default_user_profile = Cart.objects.get_or_create(user__id=1)[0]
		# default_user_profile.products.add(instance)
		# myprofile.followers.add(default_user_profile.user)
		# myprofile.followers.add(1)


post_save.connect(post_save_user_receiver, sender=Referral)