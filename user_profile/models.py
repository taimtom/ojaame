from django.db import models
from django.conf import settings

from django.template import loader
from django.core.mail import send_mail
from ojaale.settings import EMAIL_HOST_USER

from django.db.models.signals import post_save
from referal.models import Referral

User=settings.AUTH_USER_MODEL
# Create your models here.
class Notification(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    subject= models.CharField(max_length=100)
    seen=models.BooleanField(default=False)
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    def new_notifications(self):
        return self.objects.filter(seen=False)

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    gift_card=models.IntegerField(default=1000)
    image=models.ImageField(upload_to='profile/images',null=True, blank=True)
    cover=models.ImageField(upload_to='profile/images',null=True, blank=True)
    fullname=models.CharField(max_length=120, null=True, blank=True)
    details=models.TextField(null=True, blank=True)
    savings=models.IntegerField(default=100)

    def __str__(self):
       return self.user.username

def post_save_user_receiver(sender,instance,created,*args, **kwargs):


    if created:
        profile, is_created  = UserProfile.objects.get_or_create(user=instance)
        html_message = loader.render_to_string(
            'main/emails/email1/welcome-info-email.html',
            {
                'user':instance,
                
            }
        )
        send_mail("Welcome To Ojaa.me.","message",EMAIL_HOST_USER,[str(instance.email)],fail_silently=True,html_message=html_message)
		# default_user_profile = Cart.objects.get_or_create(user__id=1)[0]
		# default_user_profile.products.add(instance)
		# myprofile.followers.add(default_user_profile.user)
		# myprofile.followers.add(1)
        


post_save.connect(post_save_user_receiver, sender=User)