from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from cartapp.models import CartModel
from cartapp.forms import CartForm
from Foodapp.models import FoodModel
from django.db import connection
from django.contrib import messages


# Create your views here.
def checkQuantityBeforeAdding(request):
	foodQuantity=request.GET['foodQuantity']
	foodid=request.GET['foodIdfk']
	cursor=connection.cursor()
	quantity=cursor.execute('select quantity from Foodapp_foodmodel where id=%s',[foodIdfk])
	quantity=int(cursor.fetchone()[0])
	if int(quantity)<int(foodQuantity):
		return HttpResponse("out of stock",content_type="text/plain")
	
def showCartView(request):
	Email=request.session['Email']
	cart=CartModel.objects.raw('select c.id,f.name,c.Quantity from cart_tbl as c INNER JOIN Foodapp_foodmodel as f ON f.id=c.foodIdfk and c.emailIdfk==%s',[Email])
	return render(request,'cartapp/cart.html',{'cart':cart})

def showAddToCartView(request,id):
	form = CartForm()
	return render(request,'cartapp/addcart.html',{'form':form,'foodIdfk':id})

def addToCartView(request):
	form=CartForm()
	if request.method=='POST':
		food_id=request.POST.get('foodIdfk')
		sessionemail=request.session['Email']
		form=CartForm(request.POST)
		cart=CartModel.objects.filter(emailIdfk=sessionemail)
		food=FoodModel.objects.get(id=food_id)
		if(food.quantity > int(request.POST['Quantity'])):
			if form.is_valid():
				if cart.count()==0:
					form.save()
				else:
					for c in cart:
						if int(c.foodIdfk)==int(request.POST['foodIdfk']):
							cursor=connection.cursor()
							newQuantity=int(c.Quantity)+int(request.POST['Quantity'])
							if newQuantity <= food.quantity:
								sqlUpdate='UPDATE cart_tbl SET Quantity={0} WHERE id={1}'.format(newQuantity,c.id)
								cursor.execute(sqlUpdate)
								break
						else:
							form.save()
		else:
			messages.info(request,"Please Enter value less than food Quantity "+str(food.quantity))
			return redirect('/Foodapp/foods')
		return redirect('/Foodapp/foods')
	return render(request,'cartapp/addcart.html',{'form':form,'foodIdfk':id})
	
def deleteCartByIdView(request,id):
	cart=CartModel.objects.get(id=id)
	cart.delete()
	return redirect('/cartapp/showCart')
