# API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializers


#PYTHON

from itertools import chain

from  django.db.models import Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib.parse import quote

from django.urls import reverse

from django.db.models import Q
from django.http import HttpResponseRedirect,Http404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import View, ListView, DetailView
from django.utils import timezone

from referal.models import Referral
from .models import Products
from reviews.forms import ReviewForm
from reviews.models import Review
from cart.models import Cart
from .forms import ProductForm
from company.models import Company
from accounts.models import SaleRecord,Pack
from django.template import loader
from django.core.mail import send_mail
from ojaale.settings import EMAIL_HOST_USER

from django import template
register = template.Library()

# Create your views here.


User=get_user_model()
def index(request):
	template_name="main/index_try.html"
	shops=Company.objects.all()
	products=Products.objects.all()
	picked_products=Products.objects.all().order_by("timestamp")
	fashion_products=Products.objects.filter(category="fashion")
	furniture_products=Products.objects.filter(category="furnitures and woodwork")
	electronic_products=Products.objects.filter(category="electronics and phones")
	livestock_products=Products.objects.filter(category="pets and livestocks")
	home_products=Products.objects.filter(category="home and kitchen")
	automobile_products=Products.objects.filter(category="automibiles and industrial machines")
	health_products=Products.objects.filter(category="health and beauty")
	cart_=None
	if request.user.is_authenticated:
		request_customer=request.user
		check_referred=Referral.objects.filter(customers=request_customer)
		# if not check_referred:
		# 	referral_link=request.COOKIES['referral_link']
		# 	referrer,in_customer = Referral.objects.toggle_customer(request_customer, referral_link)
	
	

	if request.user.is_authenticated:
		cart_=get_object_or_404(Cart, user=request.user)
		sales=SaleRecord.objects.filter(user=request.user)
	context={
		"products":products,
		"shops":shops,
		"picked_products":picked_products,
		"fashion_products":fashion_products,
		"electronic_products":electronic_products,
		"livestock_products":livestock_products,
		"home_products":home_products,
		"automobile_products":automobile_products,
		"health_products":health_products,
		"furniture_products":furniture_products,
		'carts':cart_

	}
	return render(request, template_name, context)

class ProductsList(ListView):
	queryset=Products.objects.all()
	template_name='main/product/list.html'
	# for query in queryset:
	# 	reviews=[x.rating for x in Review.objects.filter(content_type=query.get_content_type)]
		
	
	# for review in reviews:
	# 	print(review)

	def get_context_data(self, *args, **kwargs):
		context=super(ProductsList,self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			cart_=get_object_or_404(Cart, user=self.request.user)
			context['carts']=cart_

		return context
	



def productdetail(request, slug=None):
	instance = get_object_or_404(Products, slug=slug)
	reviews=Review.objects.filter_by_instance(instance)
	prev_review=None
	allow_to_review=None
	if request.user.is_authenticated:
		prev_review=reviews.filter(user=request.user)
		allow_to_review=Pack.objects.filter(contents__product=instance, user=request.user)
		
	share_string= quote(instance.description)
	
	initial_data={
		"content_type":instance.get_content_type,
		"object_id":instance.id
	}
	# if request.method == "POST":
	# 	if prev_review:
	# 		form=ReviewForm(request.POST or None)
	# 		if form.is_valid():
	# 			content_data=form.cleaned_data.get("content")
	# 			rating=request.POST.get('rating')
	# 			prev_review.content=content_data
	# 			prev_review.rating=rating
	# 			prev_review.save()
	# 	else:
	form=ReviewForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type=form.cleaned_data.get("content_type")
		content_type=ContentType.objects.get(model=c_type)
		obj_id=form.cleaned_data.get("object_id")
		content_data=form.cleaned_data.get("content")
		rating=request.POST.get('rating')
		parent_obj=None
		try:
			parent_id=int(request.POST.get('parent_id'))
		except:
			parent_id=None
		if parent_id:
			parent_qs=Review.objects.filter(id=parent_id)
			if parent_qs.exists():
				parent_obj=parent_qs.first()
				print(parent_obj)
		new_review, created=Review.objects.get_or_create(
			user=request.user,
			content_type=content_type,
			object_id=obj_id,
			content=content_data,
			parent=parent_obj,
			rating=rating
			)
		reviews_count=reviews.count()
		rating=[x.rating for x in reviews]
		
		sumrating=sum(rating)
		if reviews_count >0:
			meanrating=round((sumrating/(reviews_count)),2)
			instance.rating=meanrating
			instance.save()
		product_company=instance.company
		company_products=Products.objects.filter(company=product_company)
		
		list_products_rating=[prod.rating for prod in company_products]
		
		product_company.rating=(sum(list_products_rating)/len(list_products_rating))
		product_company.save()
		

		return HttpResponseRedirect(new_review.content_object.get_absolute_url())
	
	
	

	
	
	context={
		'object':instance,
		'reviews':reviews,
		'review_form':form,
		"allow_to_review":allow_to_review
		# 'needed_record':needed_record
		# 'product_name':instance.name,
		# 'in_cart':in_cart
		
	}
	template='main/product/detail_test.html'
	return render(request,'main/product/detail.html',context)

@login_required()
def productcreate_view(request):
	if request.user.company:
		sub_category=request.POST.get("sub_category")
		form = ProductForm(request.POST,request.FILES)
		cat_filter=request.user.company.product_cat
		if form.is_valid():
			instance=form.save(commit=False)
			instance.sub_category=sub_category
			instance.category=request.user.company.product_cat
			instance.company=request.user.company
			discount=100-(((instance.price)/(instance.discounted_from))*100)
			instance.discount=discount
			instance.save()
			messages.success(request, "Successfully Created")
			html_message = loader.render_to_string(
                            'main/emails/advert-add-product.html',
                            {
                                'product':instance,
                                
                            }
                        )
			all_users=User.objects.filter(cart__advert_email_unsubscribe=False)
			email_list=[x.email for x in all_users]
			#send_mail(f"Waw!!! A New Products Has Been Added To {instance.company.name}. Check It Out Now!!!","message",EMAIL_HOST_USER,email_list,fail_silently=True,html_message=html_message)
			return HttpResponseRedirect(f'/products/{instance.slug}')
    
		context={"form":form,"title":"Add Products To Store","button":"Add","cat_filter":cat_filter}
		template_name='main/product/form.html'
		return render(request, template_name,context)
	else:
		return HttpResponseRedirect("/create/form/")
@login_required()
def productupdate_view(request, slug):
	obj=get_object_or_404(Products, slug=slug )
	sub_category=request.POST.get("sub_category")
	if request.user.company == obj.company:
		cat_filter=request.user.company.product_cat
		if request.method=='POST':
			form = ProductForm(request.POST, request.FILES, instance=obj)
			if form.is_valid():
				instance=form.save(commit=False)
				instance.sub_category=sub_category
				instance.category=request.user.company.product_cat
				instance.company=request.user.company
				discount=100-(((instance.price)/(instance.discounted_from))*100)
				instance.discount=discount
				instance.save()
				messages.success(request, "Successfully Created")
				return HttpResponseRedirect(f'/products/{instance.slug}')
		else:
			form=ProductForm(instance=obj)
		context={"form":form,"title":"Update Product ","button":"Update","cat_filter":cat_filter}
		template_name='main/product/form.html'
		return render(request, template_name,context)
	else:
		return HttpResponseRedirect("/create/form/")

@register.filter
def not_seen(things):
    return things.filter(seen=False)

#Api Views-------------------------------------------------------------------------------------------------

class ApiProductList(APIView):
    """
    List all products, or create a new product.
    """
    def get(self, request, format=None):
        products = Products.objects.all()
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiProductDetail(APIView):
    """
    Retrieve, update or delete a Product instance.
    """
    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

# def send_email(request):
#     subject = request.POST.get('subject', '')
#     message = request.POST.get('message', '')
#     from_email = request.POST.get('from_email', '')
# 	message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
# 	message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
#     if subject and message and from_email:
#         try:
#             send_mass_mail((message1, message2), fail_silently=False)
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect('/contact/thanks/')
#     else:
#         # In reality we'd use a form class
#         # to get proper validation errors.
#         return HttpResponse('Make sure all fields are entered and valid.')


