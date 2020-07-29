from django.db import models

# Create your models here.
class data(models.Model):
    dob = models.DateField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)