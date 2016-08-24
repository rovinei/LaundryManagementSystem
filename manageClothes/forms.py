from django import forms
from .models import Clothe, clothes_type

class AddClotheForm(forms.ModelForm):
	type = forms.ChoiceField(choices=clothes_type)
	image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	class Meta:
		model = Clothe
		fields = ('type','image')

		