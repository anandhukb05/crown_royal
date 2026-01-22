from django.db import models

# Create your models here.


class Procedures(models.Model):
    prodecure = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()


class Medicine(models.Model):
    medicine = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    description = models.TextField()
