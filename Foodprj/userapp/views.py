from django.shortcuts import render,redirect
from django.http import HttpResponse
from userapp.models import UserModel
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
	print("In loginView")
	userform=UserForm()
	if request.method=='POST':
		userform=UserForm(request.POST)
		if userform.is_valid():
			Email=request.POST['Email']
			Password=request.POST['Password']
			userType=request.POST['userType']
			allUsers=UserModel.objects.raw('SELECT * FROM userapp_UserModel')
			for u in allUsers:
				if u.Email==Email and u.Password==Password and u.userType==userType:
					request.session['Email']=Email
					request.session['utype']=userType
					return redirect('/Foodapp/foods')
			return render(request,'userapp/login.html',{'form':userform,'error':'Bad Credentials'})
				
	return render(request,'userapp/login.html',{'form':userform})

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
	
