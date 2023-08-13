from django.urls import path
from . import views

urlpatterns = [
    path('insert/', views.insert_plate, name='insert_plate'),
    path('display/', views.display_table, name='display_table'),
]
