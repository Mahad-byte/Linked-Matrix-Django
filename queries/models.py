from django.db import models


# Create your models here.
class Doctor(models.Model):
    name = models.CharField()
    specialization = models.CharField()
    contact_number = models.CharField()


class Nurse(models.Model):
    name = models.CharField()
    contact_number = models.CharField()


class Patient(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctors')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='nurses')
    date_admitted = models.DateTimeField(auto_now_add=True)
    
    
class Hospital(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='hpatients')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    
    
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patients')
    diagnoses = models.CharField()
    prescription = models.CharField()

