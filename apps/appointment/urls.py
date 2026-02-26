# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('edit/<int:pk>/', views.appointment_edit, name='appointment_edit'),
    path('delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),
    path('patient_search/', views.patient_search, name='patient_search')
]