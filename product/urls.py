from django.urls import path

from rest_framework import routers

router = routers.DefaultRouter()


from .views import (
	ProductsList,
	productdetail,
	productcreate_view,
	productupdate_view,
	ApiProductList,
	ApiProductDetail
    

	)
app_name="products"
urlpatterns = [
    path('', ProductsList.as_view(), name='list'),
	
	path('<slug>/',productdetail, name='detail'),
	path ('create/form/', productcreate_view, name='create'),
	path ('<slug>/update/', productupdate_view, name='update'),


	path('api/list/', ApiProductList.as_view(), name='api-list'),
	path('api/detail/<pk>/', ApiProductDetail.as_view(), name='api-detail'),
	#ProductsDetail.as_view(), name='detail'),
    
   
]
urlpatterns += router.urls