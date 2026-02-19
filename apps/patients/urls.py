# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("create/", create_patient, name="create_patient"),
    path("view/", view_patients, name="patient_view"),
    path("view/<int:pk>/", patient_profile, name="patient_profile"),
    path("vital/<int:patient_id>", vital_view, name="vital"),
    path("vital/edit/<int:pk>/", vital_edit, name="vital_edit"),
    path("vital/delete/<int:pk>/", vital_delete, name="vital_delete"),
    path("clinical/note/<int:patient_id>/", clinical_note, name="clinical_note"),
    path("clinical/note/edit/<int:pk>/", notes_edit, name="note_edit"),
    path("clinical/note/delete/<int:pk>/", notes_delete, name="note_delete"),
    path("procedure/<int:patient_id>/", add_procedure, name="add_procedure"),
    path("procedure/edit/<int:pk>/", patient_procedure_edit, name="patient_procedure_edit"),
    path("procedure/delete/<int:pk>/", patient_procedure_delete, name="patient_procedure_delete"),
    path("invoice/bill/<int:patient_id>/", patient_bill, name="patient_bill")

]
