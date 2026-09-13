from django.core.management.base import BaseCommand
from core.models import Patient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for i in range(1, 101):

            Patient.objects.create(
                name=f"Test Patient {i}",
                age=20 + (i % 50),
                phone=f"98765{i:05d}",
                gender="Male" if i % 2 == 0 else "Female"
            )

        self.stdout.write(
            self.style.SUCCESS("100 test patients created successfully!")
        )