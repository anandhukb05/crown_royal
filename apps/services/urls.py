from django.urls import path
from . import views

urlpatterns = [
    # MAIN PANEL
    path("", views.procedure_panel, name="procedure_panel"),

    # CREATE
    path("procedure/create/", views.procedure_create, name="procedure_create"),
    path("medicine/create/", views.medicine_create, name="medicine_create"),
    path("doctor/creare/", views.doctor_create, name="doctor_create"),

    # UPDATE
    path("procedure/update/<int:pk>/", views.procedure_update, name="procedure_update"),
    path("medicine/update/<int:pk>/", views.medicine_update, name="medicine_update"),
    path("doctor/update/<int:pk>/", views.doctor_update, name="doctor_update"),

    # DELETE
    path("procedure/delete/<int:pk>/", views.procedure_delete, name="procedure_delete"),
    path("medicine/delete/<int:pk>/", views.medicine_delete, name="medicine_delete"),
    path("doctor/delete/<int:pk>/", views.doctor_delete, name="doctor_delete"),


]
