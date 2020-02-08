from django.shortcuts import render,redirect
from Foodapp.models import FoodModel
from Foodapp.forms import FoodForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.
def searchFoodbyName(request,name):
	data=serializers.serialize('json',FoodModel.objects.filter(name__contains=name))
	d=json.loads(data.replace('/',''))
	return JsonResponse({'food':d})

def showAllFoodsView(request):
	foods=FoodModel.objects.all()
	return render(request,'Foodapp/foods.html',{'foods':foods})

# This method is for deleting food by id
def deleteFoodByIdView(request,id):
	print('In DeleteFoodByIdView')
	foundFood=FoodModel.objects.get(id=id)
	foundFood.delete()
	return redirect('/Foodapp/foods') #Easyway we just want give path of show all foods and redirect method

	#Anotherway using this we cant get show all food directly
	'''foods=FoodModel.objects.all()
	return render(request,'Foodapp/foods.html',{'allfoods':foods})'''



def addFoodView(request):
	print('In AddFood')
	form=FoodForm()
	
	if request.method=='POST':
		form=FoodForm(request.POST)
		
	if form.is_valid():
		form.save()
		return redirect('/Foodapp/foods')
	
	return render(request,'Foodapp/addfood.html',{'form':form})

def updateFoodByIdView(request,id):
	print("In updateFoodByIdView")
	foundfood=FoodModel.objects.get(id=id)
	form=FoodForm(instance=foundfood)
	
	if request.method=='POST':
		form=FoodForm(request.POST,instance=foundfood)
		
		if form.is_valid():
			form.save()
			return redirect('/Foodapp/foods')
	
	return render(request,'Foodapp/updatefood.html',{'form':form})
		

	
