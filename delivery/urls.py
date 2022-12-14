from django.urls import path



from django.views.generic import TemplateView
from .views import (
	checkout_view,
	checkout,
	ApiUserList,
	ApiDeliveryDetail
	
	)


app_name="delivery"
urlpatterns = [
    path('', checkout_view, name='delivery-info'),
	path('pack/checkout/', checkout, name='checkout'),
	path('api/', ApiUserList.as_view(), name='api'),
	path('api/me/', ApiDeliveryDetail.as_view(), name='api-detail'),


	
    
   
]