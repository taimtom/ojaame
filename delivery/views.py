# API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, renderers
from rest_framework.decorators import action

from .serializers import DeliverySerializers, UserSerializers


#PYTHON
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,Http404
from django.contrib import messages
from .forms import CheckoutForm
from .models import DeliveryDetails
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

from cart.models import Cart
from company.models import Company
from referal.models import Referral
# Create your views here.
context={}

@login_required()
def checkout_view(request):
  
    user_details=DeliveryDetails.objects.filter(user=request.user)
    if user_details:
      obj = get_object_or_404(DeliveryDetails, user=request.user)
      form = CheckoutForm(request.POST or None, instance = obj)
    else:
      form = CheckoutForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(f'/delivery/pack/checkout/')
        
    if form.errors:
        print(form.errors)
        context={"form":form}
    cart_=get_object_or_404(Cart, user=request.user)
    total=0
    # for product in cart_.products.all():
    #     price = product.price
    #     total= price + total
    # cart_.total=total
    # cart_.save()
    context={
    "form":form, 
    # 'subtotal':total
    }
    template_name='main/delivery/checkout_detail.html'
    return render(request, template_name,context)
  
# # update view for details 
# def update_view(request, id): 
#     # dictionary for initial data with  
#     # field names as keys 
#     context ={} 
  
#     # fetch the object related to passed id 
#     obj = get_object_or_404(GeeksModel, id = id) 
  
#     # pass the object as instance in form 
#     form = GeeksForm(request.POST or None, instance = obj) 
  
#     # save the data from the form and 
#     # redirect to detail_view 
#     if form.is_valid(): 
#         form.save() 
#         return HttpResponseRedirect("/"+id) 
  
#     # add form dictionary to context 
#     context["form"] = form 
  
#     return render(request, "update_view.html", context) 

@login_required()
def checkout(request):
    cart_=get_object_or_404(Cart, user=request.user)
    delivery=get_object_or_404(DeliveryDetails, user=request.user)
    companys=Company.objects.filter(products__salerecord__in=cart_.content.all()).distinct()
    
    delivery_price_list=[x.average_delivery_cost for x in companys]
    # delivery_price_list=[x.product.company.filter().distinct() for x in cart_.content.all()]
    delivery_price=sum(delivery_price_list)
    

        
    

    
    
    context={
        "delivery":delivery,
        "delivery_price" :delivery_price,
        'cart':cart_
        }
    
    template_name='main/delivery/checkout.html'
    return render(request, template_name,context)





#Api Views-------------------------------------------------------------------------------------------------


User=get_user_model()
class ApiUserList(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializers(users, many=True)
        return Response(serializer.data)

    
class ApiDeliveryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self):
        try:
            return DeliveryDetails.objects.get(user=self.request.user)
        except DeliveryDetails.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        delivery = self.get_object()
        serializer = DeliverySerializers(delivery)
        return Response(serializer.data)

    def put(self, request, format=None):
        delivery = self.get_object()
        serializer = DeliverySerializer(delivery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    