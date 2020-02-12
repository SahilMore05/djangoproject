from django.db import models

# Create your models here.
class OrderModel(models.Model):
	emailIdfk=models.EmailField()
	date=models.IntegerField()
	total=models.IntegerField()
	def __str__(self):
		return '{0} {1} {2}'.format(self.emailIdfk,self.date,self.total)
	class Meta:
		db_table="order_tbl"
		
