from django.urls import path, include
from django.views.generic import TemplateView


from .views import CartList,CartUpdateToggle,pay_now,DeliveryTypeApi

app_name='cart'


urlpatterns = [
   
    path('', CartList.as_view(), name='cart'),
    path('update/', CartUpdateToggle.as_view(), name='update'),
    path('delivery-type/', DeliveryTypeApi.as_view(), name='update'),
    path('pay/', pay_now, name='pay'),

    
]
