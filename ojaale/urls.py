from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns


from django.views.generic import TemplateView
from cart.views import CartToggle
from user_profile.views import RegisterView
from product.views import index
from major.views import Search
from referal.views import registerview


from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('product.urls', namespace='products')),
    path('delivery/', include('delivery.urls', namespace='delivery')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('record/', include('accounts.urls', namespace='record')),
    path('wish/', include('wish.urls', namespace='wish')),
    path('', include('company.urls', namespace='company')),
    path('referral/', include('referal.urls', namespace='referral')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('profile/', include('user_profile.urls', namespace='profile')),
    path('cart/add_cart/', CartToggle.as_view(), name='add_cart'),
    path('account/register/', RegisterView.as_view(), name='register'),
    path('store/search/', Search.as_view(), name='search'),
    path('policies/learn-more/', TemplateView.as_view(template_name="main/policies.html"), name='learn-more'),
    path('test/test/', TemplateView.as_view(template_name="main/emails/advert-add-product.html"), name='learn-more'),
   path('gift-giving/now/', TemplateView.as_view(template_name="main/squeeze/index.html"), name='learn-more'),
   
    
    path('',index , name='home'),
    
    path('account/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += router.urls