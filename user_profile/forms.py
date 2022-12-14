from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile


User=get_user_model()

class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('email', 'username')
	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2
	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user




class UserProfileForm(forms.ModelForm):
    

    class Meta:

        model=UserProfile
        fields=(
            'fullname',
            'image',
			'cover',
			'details'

        )
        labels = {
        "fullname": "Add Your Full Name",
        "image": "Add Profile Picture",
        "cover": "Add profile Cover Picture (optional)",
		"details": "Bio (optional)",
        }
        widgets={
            'fullname':forms.TextInput(attrs={'placeholder':'John Doe'}),
            'details':forms.TextInput(attrs={'placeholder':"I'm Theophilus Olaezekiel. I'm the founder of Ojaa.me and Rhemaz.social. I'm also the current co-ordinator of Youth Ablaze. I love technology and music. I'm single and fully devoted to God and the works placed in my hand...."}),
            
        }
		


    