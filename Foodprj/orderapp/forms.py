from django import forms
from orderapp.models import OrderModel

class OrderForm(forms.ModelForm):
	class Meta:
		model=OrderModel
		fields='__all__'