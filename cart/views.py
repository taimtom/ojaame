from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, renderers
from rest_framework.decorators import action


from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Cart 
from product.models import Products,ProductPriceRanges
from accounts.models import SaleRecord
from accounts.forms import SaleRecordForm
User=get_user_model()

class CartToggle(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        cart_=Cart.objects.filter(user__username__iexact=request.user)
        if cart_ is None:
          obj=Cart.objects.create(user=request.user)
        product_id=request.POST.get('product_id')
        sale_id=request.POST.get('sale_id')
        qty_product=request.POST.get('quantity_needed')
        size_product=request.POST.get('size_needed')
        color_product=request.POST.get('color_needed')
         
        if product_id:
            product_selected = get_object_or_404(Products, id=product_id)
            product_ranges = ProductPriceRanges.objects.filter(product=product_selected)
            product_sale_price = 0
            # for s
            for product_range in product_ranges:
                if int(qty_product) in range (product_range.start_quantity, product_range.stop_quantity):
                    product_sale_price=product_range.price*int(qty_product)

            instance=SaleRecord.objects.create(
                user=request.user,
                product=product_selected,
                price=product_sale_price,
                quantity=int(qty_product),
                price_per_one=round(product_sale_price/int(qty_product), 2),
                color=color_product,
                size=size_product
            )
        else:
            instance = get_object_or_404(SaleRecord, id=sale_id)

        cart_,in_cart = Cart.objects.toggle_product(instance, request.user)
        cart_=Cart.objects.get(user=request.user)
        tot=0
        for i in cart_.content.all():
            tot=tot+i.price
        cart_.total=tot
        cart_.save()
        return redirect(f"/products/{instance.product.slug}/")
        
class CartUpdateToggle(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        sale_id=request.POST.get('sale_id')
        qty_product=request.POST.get('qty')
        instance = get_object_or_404(SaleRecord, id=sale_id)
        instance.price=sale_selected.price*int(qty_product)
        instance.quantity=int(qty_product)
        instance.save()

        return redirect(f"/cart/")
        
        	

class CartList(LoginRequiredMixin, ListView):
    template_name='main/cart/detail.html'
    def get_queryset(self):
        user=self.request.user
        qs=Cart.objects.filter(user=user)
        return qs
    
    def get_context_data(self,*args,**kwargs):
        context=super(CartList, self).get_context_data(*args, **kwargs)
        cart=self.get_queryset()
        qs=Cart.objects.get(user=self.request.user)
        context['cart_list']=cart
       

        return context

def pay_now(request):
    cart=get_object_or_404(Cart, user=request.user)
    template_name="main/delivery/pay.html"
    context={
        "cart":cart
    }
    return render(request, template_name, context)


class DeliveryTypeApi(LoginRequiredMixin,APIView):
    def post(self, request, format=None):
        data=request.data
        user=request.user
        delivery_type=data.get("delivery_type")
        user.cart.delivery_type=delivery_type
        user.cart.save()
        
            
        return Response(status=status.HTTP_201_CREATED)