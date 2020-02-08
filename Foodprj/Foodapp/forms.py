from django import forms
from Foodapp.models import FoodModel

# Create your models here.
class FoodForm(forms.ModelForm):
	class Meta:
		model=FoodModel
		fields='__all__'