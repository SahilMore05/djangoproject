from django import forms
from userapp.models import UserModel

class UserForm(forms.ModelForm):
	Password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=UserModel
		fields='__all__'