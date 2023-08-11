from django.db import models

# Create your models here.
class Plate(models.Model):
    plates = models.CharField(max_length=100)