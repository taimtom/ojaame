from turtle import onclick
from django.db import models

# Create your models here.

class Services(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()

CATEGORIES=[]

class Portfoilio(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    business_name=models.CharField(max_length=200)
    services=models.ManyToManyField(Services)
    category=models.Choices(CATEGORIES)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(null=True, blank=True)
