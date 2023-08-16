# platesapp/tasks.py
from background_task import background
from platesapp.models import Plate
from django.core.mail import send_mail

@background(schedule=1)  # Check every 1 second
def check_plate_in_database(list_of_labels):
    for label in list_of_labels:
        if Plate.objects.filter(plates=label).exists():
            # Perform some action, e.g., send notification
            send_mail(
            'Matching Plate Found',
            f'A matching plate was found: {label}',
            'donjosephmukisa@gmail.com',  # Replace with your email
            ['arindaj33@gmail.com','zbagabo@gmail.com','donmukisajoseph@gmail.com'],
            fail_silently=False,
        )
            pass
