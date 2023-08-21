from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Plate(models.Model):
    plates = models.CharField(max_length=100)
    
    def __str__(self):
        return self.plates
    

#--------------------------------------------------------------------------------

class Car(models.Model):
    numberplate = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.owner,self.numberplate

class ActivatedNumberPlate(models.Model):
    numberplate = models.CharField(max_length=20)
    owner_email = models.EmailField()
    def __str__(self):
        return self.numberplate,self.owner_email

class DeletedNumberPlate(models.Model):
    numberplate = models.CharField(max_length=20)
    owner_email = models.EmailField()
    def __str__(self):
        return self.numberplate,self.owner_email

class PendingNumberPlate(models.Model):
    numberplate = models.CharField(max_length=20)
    owner_email = models.EmailField()
    def __str__(self):
        return self.numberplate,self.owner_email
