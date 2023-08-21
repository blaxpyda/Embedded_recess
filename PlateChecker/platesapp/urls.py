from django.urls import path
from . import views

urlpatterns = [
    path('insert/', views.insert_plate, name='insert_plate'),
    path('display/', views.display_table, name='display_table'),
    #path('', views.insert_plate, name='insert_plate'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('car-registration/', views.car_registration_view, name='car_registration'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),
    
    
]
