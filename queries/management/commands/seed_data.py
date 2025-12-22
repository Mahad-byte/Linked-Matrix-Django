from django.core.management.base import BaseCommand
from faker import Faker
import random

from queries.models import (
    Doctor,
    Nurse,
    Patient,
    Hospital,
    MedicalRecord
)

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with fake hospital data"

    def add_arguments(self, parser):
        parser.add_argument('--doctors', type=int, default=5)
        parser.add_argument('--nurses', type=int, default=5)
        parser.add_argument('--patients', type=int, default=20)

    def handle(self, *args, **kwargs):
        doctors_count = kwargs['doctors']
        nurses_count = kwargs['nurses']
        patients_count = kwargs['patients']

        # Create Doctors
        doctors = []
        for _ in range(doctors_count):
            doctor = Doctor.objects.create(
                name=fake.name(),
                specialization=fake.job(),
                contact_number=fake.phone_number()
            )
            doctors.append(doctor)

        # Create Nurses
        nurses = []
        for _ in range(nurses_count):
            nurse = Nurse.objects.create(
                name=fake.name(),
                contact_number=fake.phone_number()
            )
            nurses.append(nurse)

        # Create Patients, Hospitals & Medical Records
        for _ in range(patients_count):
            doctor = random.choice(doctors)
            nurse = random.choice(nurses)

            patient = Patient.objects.create(
                name=fake.name(),
                age=random.randint(1, 100),
                doctor=doctor,
                nurse=nurse
            )

            Hospital.objects.create(
                patient=patient,
                doctor=doctor,
                nurse=nurse
            )

            MedicalRecord.objects.create(
                patient=patient,
                diagnoses=fake.sentence(nb_words=4),
                prescription=fake.sentence(nb_words=6)
            )

        self.stdout.write(self.style.SUCCESS("Fake hospital data created successfully!"))
