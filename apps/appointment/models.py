from django.db import models
from apps.patients.models import PatientProfile
from apps.services.models import Doctor


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)

    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='waiting'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date')  # prevents same doctor same day booking

    def __str__(self):
        return f"{self.patient} - {self.date}"
