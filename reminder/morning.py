# from django.db import models
# from product.models import Products
# from django.conf import settings
# from django.db.models.signals import pre_save, post_save
# from django.shortcuts import render,get_object_or_404
# from cart.models import Cart
# from django.contrib.auth.mixins import LoginRequiredMixin
# # Create your views here.
# from .models import SaleRecord,Pack
# from .serializers import SaleRecordSerializer,PackSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import datetime
# from django.views.generic import View, ListView, DetailView

# from django.template import loader
# from django.core.mail import send_mail
from ojaale.settings import EMAIL_HOST_USER
User=settings.AUTH_USER_MODEL

send_mail("New product Request Made","message",EMAIL_HOST_USER,["theophilusolaezekiel@gmail.com"])

