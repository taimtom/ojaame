from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from .views import mynotifications,profileupdate_view

app_name='profile'


urlpatterns = [
    path('email-test/',TemplateView.as_view(template_name='main/emails/email1/welcome-info-email.html'), name="update"),
   path('update/',profileupdate_view, name="update"),
    path('notifications/', mynotifications, name='notifications'),
    #  path(
    #     'change-password/',
    #     auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'),
    # ),
    # path(
    #     'password_reset/',
    #     auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
    # ),
    # path(
    #     'change-password/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name='change-password.html'),
    # ),
    
    
    
    
    
]