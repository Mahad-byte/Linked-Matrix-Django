from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from queries.models import Patient, Doctor
from logging import getLogger
import requests
from content_website.settings import webhook_url

@shared_task
def delete_patients_week_old():
    week_older = timezone.now() - timedelta(days=7)
    Patient.objects.filter(date_admitted__lte=week_older).delete()
    print("week older: ", week_older)
    print("Deleted")
    logger = getLogger('request_logger')
    logger.info("Deleted Patients!!!!!!!!!")


@shared_task
def send_info_to_discord():
    patient_of_all_doctors = Doctor.objects.prefetch_related('doctors').all()
    message = "**Doctor Patient Report**\n\n"
    for details in patient_of_all_doctors:
        doctor_name = details.name
        patients = details.doctors.all()
        
        message += f"**Dr. {doctor_name}:**\n"
        
        for patient in patients:
                patient_name = patient.name or f"Patient #{patient.id}"
                date_str = patient.date_admitted.strftime("%b %d")
                
                message += f"• {patient_name} ({date_str})\n"
            
        
        message += "\n"  
    
    send_to_discord(message)
    return "Report sent!"

        
def send_to_discord(text):
    
    data = {"content": text}
    response = requests.post(webhook_url, json=data)
    if response:
        logger = getLogger('request_logger')
        logger.info("Sent WEbhook to Discord!!!!!!!!!")
    else:
        print("Invalid webhook_url")