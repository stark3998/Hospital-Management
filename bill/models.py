from django.db import models
from django.contrib.auth.models import User
from case.models import case
from stock.models import items

# Create your models here.
class bill(models.Model):
	case = models.ForeignKey(case, on_delete=models.CASCADE, related_name='bill_case')
	ammount = models.IntegerField()
	item = models.ForeignKey(items, on_delete=models.CASCADE, related_name='bill_item')
	quantity = models.IntegerField()
	bill_date = models.DateField()
	bill_details = models.CharField(max_length=200)
	is_paid = models.BooleanField(default=False)

	def __str__(self):
		return self.case.patient.username
