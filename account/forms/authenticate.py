from django import forms

class AuthenticationForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput,label="Username")
	password = forms.CharField(widget=forms.PasswordInput,label="Password")

	class Meta:
		fields = ['username','password']