from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CarRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
from .models import Plate
from .tasks import check_plate_in_database


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


#Sign Up
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with the actual URL name for the dashboard page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})




#login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with the actual URL name for the dashboard page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})




#Registering a aar
@login_required
def car_registration_view(request):
    if request.method == 'POST':
        form = CarRegistrationForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('dashboard')  # Replace 'dashboard' with the actual URL name for the dashboard page
    else:
        form = CarRegistrationForm()
    return render(request, 'car_registration.html', {'form': form})




@staff_member_required
def admin_dashboard_view(request):
    return render(request, 'admin_dashboard.html')


check_plate_in_database()