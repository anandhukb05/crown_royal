# urls.py
from django.urls import path
from . import views

urlpatterns = [

    path("appointment/", views.appointment_list, name="appointment_list"),

    path("appointment/add/", views.appointment_add, name="appointment_add"),

    path("appointment/delete/<int:pk>/",
         views.appointment_delete,
         name="appointment_delete"),

    path("appointment/reschedule/<int:pk>/",
         views.appointment_reschedule,
         name="appointment_reschedule"),

    path("appointment/confirm/<int:pk>/",
         views.appointment_confirm,
         name="appointment_confirm"),
]
