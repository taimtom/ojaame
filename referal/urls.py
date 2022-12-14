from django.urls import path

from .views import (
	Dashboard,
	SendReferralEmail,
    ReferralCreate,
	registerview,
	ReferralDashboardViev,
	withdrawal,
	ApiReferralDetail
	
    

	)
app_name="referral"
urlpatterns = [
	
	path('<username>/',Dashboard.as_view(), name='detail'),
	path ('create/form/', ReferralCreate.as_view(), name='create'),
	path ('email/send/', SendReferralEmail.as_view(), name='send-email'),
	path ('<referral_link>/register/', registerview, name='register'),
	path ('s/api/', ReferralDashboardViev.as_view()),
	path ('s/api/me/', ApiReferralDetail.as_view()),
	#path ('sale/api/', SaleRecordAPIViewDashboard.as_view()),
	path ('user/withdraw/', withdrawal, name="withdraw")
	 
]