# API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ReferralSerializers
from delivery.serializers import UserSerializers
#PYTHON
from django.http import JsonResponse,HttpResponseRedirect, Http404
from  django.db.models import Count
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import random
import string

from django.conf import settings


from django.template import loader
from django.core.mail import send_mail
from ojaale.settings import EMAIL_HOST_USER

# Create your views here.

from .models import Referral,Account,WidrawalRequest
from user_profile.forms import UserCreationForm
from .forms import WithdrawalForm

User=get_user_model()


class SendReferralEmail(APIView):
    def post(self, request, format=None):
        data=request.data
        user=request.user
        referrer=Referral.objects.filter(user=request.user)
        email_addresses=data.get("email_addresses")
        address=email_addresses.split(';')
       
        
        html_message = loader.render_to_string(
            'main/emails/email1/referral-email.html',
            {
                'user':user,
                'referral':referrer
                
            }
        )
        send_mail(f"{user.username.capitalize()} Just Sent You N1000 Gift Card","message",EMAIL_HOST_USER,address,fail_silently=True,html_message=html_message)
        return Response(status=status.HTTP_201_CREATED)
class Dashboard(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        print(request.user)
        instance=get_object_or_404(Referral, user=request.user)
        test_product=instance.customers.all().extra({'date_joined':"date(date_joined)"}).values('date_joined').annotate(created_count=Count('id'))
        test_listing=[]
        for u in test_product:
            for key, value in u.items():
                test_listing.append(value)
        test_days=test_listing[::2]
        test_users=test_listing[1::2]
        total_ammount_request=0
        context={
            'instance':instance,
            'user':request.user,
        }
        if instance.account:
            profit=get_object_or_404(Account, referrer=instance)
            context['profit']=profit
        template_name='dashboard.html'
        return render(request, template_name,context)
def withdrawal(request):
    instance=get_object_or_404(Referral, user=request.user)
    profit=get_object_or_404(Account, referrer=instance)
    withdrawal_requests=WidrawalRequest.objects.filter(user=instance)
    form=WithdrawalForm(request.POST)
    if form.is_valid():
        instances=form.save(commit=False)
        instances.user=instance
        if int(instances.ammount_request) >= profit.available_balance:
            messages.error(request, 'Insufficient Balance')
            return  HttpResponseRedirect(instance.get_absolute_url())
        else:    
            
            account=Account.objects.get(referrer=instances.user)
            account.available_balance = account.available_balance-int(instances.ammount_request)
            account.save()
            instances.save()
            messages.success(request, 'Successfully sent')
            return  HttpResponseRedirect(instance.get_absolute_url())
class ReferralCreate(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.user.userprofile.fullname == None:
            return redirect(f"/profile/update/")
        referral_=Referral.objects.filter(user__username__iexact=request.user.username)
        size=20
        chars=string.ascii_lowercase + string.digits
        if not referral_:
            obj=Referral.objects.create(
            user=request.user,
            referral_link=str(request.user.username)+''.join(random.choice(chars) for _ in range(size)),
            mygain=0
            )
            return redirect(f"/referral/{request.user.username}/")
        else:
            return redirect(f"/referral/{request.user.username}/")
def registerview(request, referral_link=None):
    
    
    form = UserCreationForm(request.POST or None, request.FILES or None)
    referred_by=Referral.objects.get(referral_link=referral_link)
    # user=User.objects.filter(user__referral__referral_link=referral_link)
    if form.is_valid():
        instance=form.save(commit=False)
        request_customer = instance
        instance.save()
        
         
        return HttpResponseRedirect("/accounts/login/")   
    context={
        'title':f'{referred_by.user.username.capitalize()} Wants You To Sign Up To Recieve The Gift Card',
        'action':'register',
        'register_form':form
    }
    template_name = 'registration/register.html'
    full_path=request.get_full_path()
    referral_link=full_path.split('/')[2]
    response= render(request, template_name, context)
    response.set_cookie('referral_link',referral_link)
    return response
    


#Api-------------------------------------------------------------------------------------------------------------
class ReferralDashboardViev(APIView):
    def get(self,*args,**kwargs):
        instance=get_object_or_404(Referral, user=self.request.user)
        referred=instance.customers.all()
        test_product=instance.customers.all().extra({'date_joined':"date(date_joined)"}).values('date_joined').annotate(created_count=Count('id'))
        test_listing=[]
        for u in test_product:
            for key, value in u.items():
                test_listing.append(value)
        test_days=test_listing[::2]
        test_users=test_listing[1::2]
        print(test_days, test_users)
        data={
            "days":test_days,
            "customers":test_users
        }
        serializer=UserSerializers(referred,many=True)
        return Response(data)

# class ApiProductList(APIView):
#     """
#     List all products, or create a new product.
#     """
#     def get(self, request, format=None):
#         products = Products.objects.all()
#         serializer = ProductSerializers(products, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ProductSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiReferralDetail(APIView):
    """
    Retrieve, update or delete a Referral instance.
    """
    def get_object(self):
        try:
            return Referral.objects.get(user=self.request.user)
        except Referral.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        referral = self.get_object()
        serializer = ReferralSerializers(referral)
        return Response(serializer.data)

    def put(self, request, format=None):
        referral = self.get_object()
        serializer = ReferralSerializer(referral, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    