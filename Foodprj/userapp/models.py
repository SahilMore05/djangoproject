from django.db import models

# Create your models here.
class UserModel(models.Model):
	utypes=[('User','User'),('Admin','Admin')]
	Email = models.CharField(max_length=20)
	Password = models.CharField(max_length=15)
	userType=models.CharField(max_length=15,choices=utypes)
	
	def __str__(self):
		return '{0} {1}'.format(self.Email,self.Password)