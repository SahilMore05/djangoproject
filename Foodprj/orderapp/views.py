from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
import datetime
from cartapp.models import CartModel
from Foodapp.models import FoodModel
from orderapp.models import OrderModel
from orderapp.forms import OrderForm

# Create your views here.
def showOrderView(request):
	Email = request.session['Email']
	orderDate= datetime.date.today()
	orders = OrderModel.objects.filter(emailIdfk=Email)
	print(orders)
	return render(request,'orderapp/order.html',{'orders':orders})

def placeOrderView(request):
	form=OrderForm()
	if request.method=='POST':
		Email=request.session['Email']
		orderDate=datetime.date.today()
		cursor=connection.cursor()
		tbill=cursor.execute('SELECT SUM(f.price*c.Quantity) FROM Foodapp_foodmodel as f INNER JOIN cart_tbl as c ON f.id=c.foodIdfk and c.emailIdfk=%s',[Email])
		total=float(cursor.fetchone()[0])
		insertSql='INSERT INTO order_tbl(total,date,emailIdfk) values ("%f","%s","%s")'%(total,orderDate,Email)
		cursor.execute(insertSql)
		cart=CartModel.objects.all()
		food=FoodModel.objects.all()
		for c in cart:
			for f in food:
				if int(c.foodIdfk)==int(f.id):
					newQuantity=int(f.quantity)-int(c.Quantity)
					if newQuantity>0:
						
						sqlupdate="UPDATE Foodapp_foodmodel SET quantity={0} WHERE id={1}".format(newQuantity,f.id)
					else:
						print("Item finished")
						newQuantity=0
						sqlupdate="UPDATE Foodapp_foodmodel SET quantity={0} WHERE id={1}".format(newQuantity,f.id)
					cursor.execute(sqlupdate)
		CartModel.objects.filter(emailIdfk=Email).delete()
		return redirect('/Foodapp/foods')
	return render(request,'orderapp/order.html',{'form':form})
	
def deleteOrder(request,id):
	print('deleteUserByIdView')
	foundOrder=OrderModel.objects.get(id=id)
	foundOrder.delete()
	return redirect('/orderapp/order')
