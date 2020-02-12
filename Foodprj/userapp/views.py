from django.shortcuts import render,redirect
from django.http import HttpResponse
from userapp.models import UserModel,AdminModel
from userapp.forms import UserForm

# Create your views here.
def showAllUserView(request):
	users = UserModel.objects.all()
	return render(request,'userapp/users.html',{'users':users})

# This method is for deleting user by id
def deleteUserByIdView(request,id):
	print('In DeleteUserByIdView')
	foundUser=UserModel.objects.get(id=id)
	foundUser.delete()
	return redirect('/userapp/users')

def addUserView(request):
	print('In AddUser')
	form=UserForm()
	
	if request.method=='POST':
		form=UserForm(request.POST)
		
	if form.is_valid():
		form.save()
		return redirect('/userapp/users')
	
	return render(request,'userapp/register.html',{'form':form})

def updateUserByIdView(request,id):
	print("In updateUserByIdView")
	foundUser=UserModel.objects.get(id=id)
	form=UserForm(instance=foundUser)
	
	if request.method=='POST':
		form=UserForm(request.POST,instance=foundUser)
		
		if form.is_valid():
			form.save()
			return redirect('/userapp/users')
	
	return render(request,'userapp/updateuser.html',{'form':form})

def loginView(request):
	form=UserForm()
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			print("valid")
			Email=request.POST['Email']
			Password=request.POST['Password']
			userType=request.POST['utype']
			if userType == "admin" :
				print("in admin")
				admin=AdminModel.objects.raw('select * from userapp_AdminModel')
				for a in admin:
					if a.Email==Email and a.Password==Password:
						request.session['Email']=Email
						request.session['utype']="admin"
						return redirect('/Foodapp/foods')
			elif userType == "user":
				allusers=UserModel.objects.raw('select * from userapp_UserModel')
				for u in allusers:
					#if u.email==email and u.password==password and u.utype==userType:
					if u.Email==Email and u.Password==Password:	
						request.session['Email']=Email
						request.session['utype']="user"
						print(request.session['utype'])
						return redirect('/Foodapp/foods')
				return render(request,'userapp/login.html',{'form':form,'error':'Bad credentials'})	
			else:
				return render(request,'userapp/login.html',{'form':form,'error':'Bad credentials'})
		#else:
			#print("Hi...")
	return render(request,'userapp/login.html',{'form':form})


def logoutView(request):
	request.session.clear()
	return redirect('/Foodapp/foods')
	
def sameEmailView(request):
	users = UserModel.objects.all()
	print(request.GET['Email'])
	users = UserModel.objects.filter(email=request.GET['Email'])
	if users.count()!=0:
		return HttpResponse('Already exists',content_type = 'text/plain')
	return HttpResponse('ok',content_type='text/plain')
	
