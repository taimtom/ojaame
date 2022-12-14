from django.urls import path


from django.views.generic import TemplateView
from .views import (
CompanyProfile,
companycreate_view,
companyupdate_view,
Companies,
ApiCompanyList,
ApiCompanyDetail,
companyaccount,
companybankaccount
# productscreate_view
	)
app_name="company"
urlpatterns = [
	path('companies/',Companies.as_view(), name='list'),
	path('<slug>/',CompanyProfile.as_view(), name='detail'),
	path('<slug>/account/',companyaccount, name='detail-account'),
	path('company/bank-info/',companybankaccount, name='bank-detail'),
	path('<slug>/delivered/',CompanyProfile.as_view(template_name="main/company/delivered.html"), name='detail-delivered'),
	path('<slug>/returned/',CompanyProfile.as_view(template_name="main/company/returned.html"), name='detail-returned'),
	path('<slug>/requested/',CompanyProfile.as_view(template_name="main/company/requested.html"), name='detail-requested'),
	path('<slug>/shiped/',CompanyProfile.as_view(template_name="main/company/shiped.html"), name='detail-shiped'),
	path('create/form/',companycreate_view, name='create'),
	path('update/form/',companyupdate_view, name='update'),
    path('api/list/',ApiCompanyList.as_view(), name='api-list'),
	path('api/<slug>/',ApiCompanyDetail.as_view(), name='api-detail'),
   
]