from django.shortcuts import render, redirect
# Create your views here.
from .models import Plate
from .tasks import check_plate_in_database
import logging

def insert_plate(request):
    if request.method == 'POST':
        plate_value = request.POST['plate_value']
        Plate.objects.create(plates=plate_value)
        check_plate_in_database(plate_value)  # Trigger background task
        return redirect('display_table')
    return render(request, 'insert_plate.html')

def display_table(request):
    plates = Plate.objects.all()
    return render(request, 'display_table.html', {'plates': plates})

check_plate_in_database()