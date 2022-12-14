from django.urls import path, include
from django.views.generic import TemplateView


from django.views.generic import TemplateView
from .views import SaleRecordApi,PackApi,DeliveryResponseApi,CustomerResponseApi, MyPack

app_name='accounts'


urlpatterns = [
   
    path('sale/', SaleRecordApi.as_view(), name='sale-record'),
    path('pack/', PackApi.as_view(), name='pack-record'),
    path('delivery-company/', DeliveryResponseApi.as_view(), name='delivery-company'),
    path('customer-response/', CustomerResponseApi.as_view(), name='user-response'),
    path('my-pack/', MyPack.as_view(template_name="main/pack/customer_response.html"), name='my-pack'),
    path('my-pack/shipped/', MyPack.as_view(template_name="main/pack/shipped.html"), name='my-pack-shipped'),
    path('my-pack/delivered/', MyPack.as_view(template_name="main/pack/delivered.html"), name='my-pack-delivered'),
    path('my-pack/requested/', MyPack.as_view(template_name="main/pack/requested.html"), name='my-pack-requested'),
    path('my-pack/returned/', MyPack.as_view(template_name="main/pack/returned.html"), name='my-pack-returned'),
    
]
