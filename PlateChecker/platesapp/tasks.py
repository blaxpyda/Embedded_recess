# platesapp/tasks.py
from background_task import background
from platesapp.models import Plate

@background(schedule=1)  # Check every 5 seconds
def check_plate_in_database(value):
    if Plate.objects.filter(plates=value).exists():
        # Perform some action, e.g., send notification
        pass
