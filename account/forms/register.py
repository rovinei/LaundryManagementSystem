from django import forms
from account.models import User, Gender

class RegistrationForm(forms.ModelForm):
	"""
	HTML form for user registration
	"""

	username = forms.CharField(widget=forms.TextInput,label="Username")
	firstname = forms.CharField(widget=forms.TextInput,label="First Name")
	lastname = forms.CharField(widget=forms.TextInput,label="Last Name")
	gender = forms.ChoiceField(choices=Gender,label="Gender")
	email = forms.EmailField(widget=forms.TextInput,label="Email")
	phonenumber = forms.IntegerField(widget=forms.TextInput,label="Phone Number")
	#profilepic = forms.ImageField()
	password1 = forms.CharField(widget=forms.PasswordInput,label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput,label="Password (Re-type)")

	class Meta:
		model = User
		fields = ('username','firstname','lastname', 'gender','email','phonenumber','password1','password2')

	def clean(self):
		cleaned_data = super(RegistrationForm,self).clean()
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Password doesn't match!")
			return self.cleaned_data

	def save(self,commit=True):
		user = super(RegistrationForm,self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()

		return user


