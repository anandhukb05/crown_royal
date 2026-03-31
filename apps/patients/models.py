from django.db import models
import os
from apps.services.models import Procedures, Medicine
# Create your models here.


class PatientProfile(models.Model):
    patient_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    age = models.IntegerField()
    aadhaar_id = models.BigIntegerField()
    phno = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=75, unique=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    pincode = models.CharField(max_length=20)
    image_path = models.ImageField(upload_to="patients/", blank=True, null=True)
     

class Vital(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    sugar = models.FloatField(null=True, blank=True)
    systolic = models.IntegerField(null=True, blank=True)
    diastolic = models.IntegerField(null=True, blank=True)
    pulse = models.IntegerField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)
    respiratory = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# class Appointment(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # date = models.DateTimeField()

class ClinicalNotes(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    notes = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)


class PatientProcedure(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    added_date = models.DateTimeField(null=True, blank=True)
    procedure = models.ForeignKey(Procedures, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    notes = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=15)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)


class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    next_review_date = models.DateTimeField(null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    strength = models.CharField(max_length=150)
    strength_unit = models.CharField(max_length=100)
    duration = models.IntegerField(null=True, blank=True)
    duration_period = models.CharField(max_length=50)
    morning = models.IntegerField(null=True, blank=True)
    noon = models.IntegerField(null=True, blank=True)
    night = models.IntegerField(null=True, blank=True)
    after_food = models.BooleanField(default=True)
    usage = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)


def patient_gallery_path(instance, filename):
    return f"patients/{instance.patient.patient_id}/{filename}"


class Gallery(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to=patient_gallery_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def is_image(self):
        return self.file.name.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".webp")
        )
