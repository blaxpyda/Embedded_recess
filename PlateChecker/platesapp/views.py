from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import CarRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Car,PendingNumberPlate, DeletedNumberPlate, ActivatedNumberPlate
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
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})




#login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:
                return redirect('user_dashboard')  # Redirect to normal user dashboard
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
            return redirect('user_dashboard')  # Replace 'dashboard' with the actual URL name for the dashboard page
    else:
        form = CarRegistrationForm()
    return render(request, 'car_registration.html', {'form': form})






@staff_member_required
def admin_dashboard_view(request):
    pending_number_plates = PendingNumberPlate.objects.all()
    deleted_number_plates = DeletedNumberPlate.objects.all()
    users_with_number_plates = []

    for user in User.objects.all():
        user_info = {'user': user, 'number_plates': Car.objects.filter(owner=user)}
        users_with_number_plates.append(user_info)

    context = {
        'pending_number_plates': pending_number_plates,
        'deleted_number_plates': deleted_number_plates,
        'users_with_number_plates': users_with_number_plates
    }
    return render(request, 'admin_dashboard.html', context)




@login_required
def user_dashboard_view(request):
    user_cars = Car.objects.filter(owner=request.user)
    context = {'user_cars': user_cars}
    return render(request, 'user_dashboard.html', context)

check_plate_in_database()