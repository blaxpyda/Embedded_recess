from django.contrib import admin
from .models import Plate,PendingNumberPlate,ActivatedNumberPlate
# Register your models here.
admin.site.register(Plate)
admin.site.register(PendingNumberPlate)

admin.site.register(ActivatedNumberPlate)

