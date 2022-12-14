from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.http import Http404
from django.views.generic import DetailView,ListView,View,CreateView,UpdateView
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from ojaale.settings import EMAIL_HOST_USER


from .forms import UserCreationForm, UserProfileForm
from .models import Notification, UserProfile
# Create your views here.
def activate_user_view(request, code=None,*args,**kwargs):
	if code:
		qs=MyProfile.objects.filter(activation_key=code)
		if qs.exists() and qs.count()==1:
			myprofile=qs.first()
			if not myprofile.activated:
				user_=myprofile.user
				user_.is_active=True
				user_.save()
				myprofile.activated=True
				myprofile.activation_key=None

				myprofile.save()
				return redirect("/login/")
	return redirect('/login/')




def send_notification(user,message, subject, reciever):

    
	send_mail(subject, message, EMAIL_HOST_USER, [str(reciever)])
	new_notification=Notification.objects.create(
		user=user,
		subject=subject,
		message=message,
		reciepient=reciever

	)
	return HttpResponse('Email Sent')
@login_required()
def mynotifications(request):
	qs=Notification.objects.all()
	new_notifications=Notification.objects.filter(seen=False)
	for obj in new_notifications:
		obj.seen=True
		obj.save()
	template_name="main/profile/notifications.html"
	context={
		"notifications":qs
	}
	return render(request,template_name, context)




def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
class RegisterView(SuccessMessageMixin,CreateView):
	form_class=UserCreationForm
	template_name = 'registration/register.html'
	success_url = '/account/login/'
	success_message="<tab> User successfully created, you can now Login.</tab>"
	
	def get_context_data(self,*args, **kwargs):
		context=super(RegisterView,self).get_context_data(*args,**kwargs)
		form = UserCreationForm(self.request.POST or None, self.request.FILES or None)
		context['register_form']=form
		context['title']='Sign Up'
		context['action']='register'
		return context
    #def dispatch(self,*args,**kwargs):
    #	if self.request.user.is_authenticated():
    #		return redirect('/logout/')
    #	return super(RegisterView,self).dispatch(*args,**kwargs)
@login_required()
def profileupdate_view(request):
	obj=get_object_or_404(UserProfile, user=request.user )
	if request.method=='POST':
		form = UserProfileForm(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.save()
			messages.success(request, "Successfully Created")
			return HttpResponseRedirect(f'/referral/create/form/')
	else:
		form=UserProfileForm(instance=obj)
	context={"form":form,"title":"Update Profile ","button":"Update"}
	template_name='main/profile/form.html'
	return render(request, template_name,context)
	
