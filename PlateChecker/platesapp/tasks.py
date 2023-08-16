# platesapp/tasks.py
from background_task import background
from platesapp.models import Plate

@background(schedule=1)  # Check every 1 second
def check_plate_in_database(list_of_labels):
    for label in list_of_labels:
        if Plate.objects.filter(plates=label).exists():
            # Perform some action, e.g., send notification
            
            pass
