from itertools import chain

from django.core.paginator import Paginator


# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from django.http import HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth import get_user_model

from product.models import Products
from cart.models import Cart
from company.models import Company
from user_profile.models import UserProfile

from django.template import loader
from django.core.mail import send_mail
from ojaale.settings import EMAIL_HOST_USER

import datetime
import time
# Create your views here.
User=get_user_model()
def index(request):
	template_name="main/index_try.html"
	shops=Company.objects.all()
	products=Products.objects.all()
	picked_products=Products.objects.all().order_by("-timestamp")
	cart_=None
	print(request.user.is_authenticated)
	if request.user.is_authenticated:
		cart_=get_object_or_404(Cart, user=request.user)
	context={
		"products":products,
		"picked_products":picked_products,
		"shops":shops,
		'carts':cart_

	}
	return render(request, template_name, context)

class Search(View):
	def get(self,request,*args,**kwargs):
		shops=Company.objects.all()
		products=Products.objects.all()
		query=request.GET.get('search')
		category_search=request.GET.get('cat_q')
		
		if query:
			query=query.strip()
			# vector=SearchVector('name', weight='A')+SearchVector('brand', weight='B')
			# vector1=SearchVector('name', weight='A')+SearchVector('product_cat', weight='B')
			# word=SearchQuery(query)
			# shops=Company.objects.annotate(search=SearchQuery(query, search_type='phrase'))
			# products=Products.objects.annotate(rank=SearchRank(vector, word))
			shops=shops.search(query)
			products=products.search(query)
		if category_search:
			category_search=category_search.strip()
			shops=shops.search(category_search)
			products=products.cat_search(category_search)
		context={
			'shops':shops,
			'products':products,
			'query':query,
			'category_search':category_search,
		}
		template_name='main/search/search.html'
		return render(request, template_name, context)
def daily_mails():
	users=User.objects.all()
	for user in users:
		joined_on=user.date_joined
		users_profile=UserProfile.objects.filter(user=user)
		if not users_profile:
			pass
		else:
			if user.userprofile.gift_card == 1000:
				fourteen_day_interval=datetime.timedelta(days=14)
				gift_expires_on=joined_on+fourteen_day_interval
				now=datetime.datetime.now()
				expired=now.timestamp()  -gift_expires_on.timestamp()
				if expired >0:
					# user.userprofile.gift_card=0
					# user.userprofile.save()
					html_message = loader.render_to_string(
						'main/emails/email1/general-email.html',
						{
							# 'company': company,
							'subject':  f'Hello {user.username}. Your Gift Card Will Soon Expire. Quickly Use It Now!!! ',
							'message':f"The Gift Card Expires On {gift_expires_on}. Use It Now!!!",
							"button":"Use Gift Card",
							"button_link":"https://ojaa.me/products"
							
						}

					)
					send_mail(f"Hello {user.username}","message",EMAIL_HOST_USER,[str(user.email)],fail_silently=True,html_message=html_message)
				if expired <= 0:
					html_message = loader.render_to_string(
						'main/emails/email1/general-email.html',
						{
							# 'company': company,
							'subject':  f'Good Morning {user.username}. How was Your Night? I Hope I Was Blissful? ',
							'message':f"Get Items You Need To Make Your Day Very Colorful And Effective Now",
							"button":"Get Them Now!!",
							"button_link":"https://ojaa.me/products"
							
						}

					)
					send_mail(f"Hello {user.username}","message",EMAIL_HOST_USER,[str(user.email)],fail_silently=True,html_message=html_message)

				
			# html_message = loader.render_to_string(
			# 	'main/emails/email1/general-email.html',
			# 	{
			# 		# 'company': company,
			# 		'subject':  f'Hello {user.username}. Your Gift Card Will Soon Expire. Quickly Use It Now!!! ',
			# 		'message':f"The Gift Card Expires On {gift_expires_on}. Use It Now!!!",
					
			# 	}
			# )
			# send_mail(f"Hello {user.username}","message",EMAIL_HOST_USER,[str(user.email)],fail_silently=True,html_message=html_message)
		user_company=Company.objects.filter(owner=user)
		if not user_company:
			pass
		else:
			if user.company:
				html_message = loader.render_to_string(
					'main/emails/email1/general-email.html',
					{
						'company': user.campany.name,
						'subject':  f'Hello {user.campany.name}. Have You Added More Items To Your Store Today?  ',
						'message':f"People visiting your store haven't seen what they would like to buy yet. Add more products now!!!",
						"button":"Add Products Now!!",
						"button_link":"https://ojaa.me/products/create/form"
						
					}
				)
				send_mail(f"Hello {user.campany.name}","message",EMAIL_HOST_USER,[str(user.campany.email)],fail_silently=True,html_message=html_message)
			
# def send_email_at(send_time):
# 	time.sleep(send_time.timestamp()-time.time())
# 	daily_mails()

# first_email_time=datetime.datetime(2021,1,26,11,50,0)
# interval=datetime.timedelta(days=1)

# send_time=first_email_time

# while True:
# 	send_email_at(send_time)
# 	send_time=send_time+interval	