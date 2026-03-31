# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("create/", create_patient, name="create_patient"),
    path("view/", view_patients, name="patient_view"),
    path("patients/edit/<int:pk>/", edit_patient, name="edit_patient"),
    path("patients/delete/<int:pk>/", delete_patient, name="delete_patient"),
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
    path("prescription/add/<str:patient_id>/", add_prescription, name="add_prescription"),
    path("prescription/edit/<int:pk>/", prescription_edit, name="prescription_edit"),
    path("prescription/delete/<int:pk>/", prescription_delete, name="prescription_delete"),
    path("invoice/bill/<int:patient_id>/", patient_bill, name="patient_bill"),
    path("invoice/<int:patient_id>/", add_invoice, name="add_invoice"),
    path("gallery/upload/<int:patient_id>/", upload_gallery, name="upload_gallery"),
    path("gallery/delete/<int:pk>/", delete_gallery, name="delete_gallery"),

]
