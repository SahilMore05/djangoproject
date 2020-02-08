from django.db import models

# Create your models here.
class CartModel(models.Model):
	foodIdfk=models.IntegerField()
	Quantity=models.IntegerField()
	emailIdfk=models.EmailField()
	def __str__(self):
		return '{0} {1} {2}'.format(self.foodIdfk,self.Quantity,self.emailIdfk)
	class Meta:
		db_table="cart_tbl"