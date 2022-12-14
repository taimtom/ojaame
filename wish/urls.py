from django.urls import path
from django.views.generic import TemplateView


from .views import WishList,WishToggle,ApiWishList

app_name='wish'


urlpatterns = [
   
    path('', WishList.as_view(), name='wish'),
    path('add_cart/', WishToggle.as_view(), name='favourite'),
    path ('api/', ApiWishList.as_view()),
    
]
