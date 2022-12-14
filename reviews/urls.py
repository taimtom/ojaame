from django.urls import path

from .views import (
	ApiReviewList,
	ApiReviewDetail
	
    

	)
app_name="reviews"
urlpatterns = [
	
	path ('api/', ApiReviewList.as_view()),
	path ('api/<pk>/', ApiReviewDetail.as_view()),
	
	 
]