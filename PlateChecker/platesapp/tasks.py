# platesapp/tasks.py
from django_background_tasks4 import 
from platesapp.models import Plate
from django.core.mail import send_mail
from .models import Plate
from platesapp.models import ActivatedNumberPlate
#------------------------------------------------------------------------------
import serial
import numpy as np
import cv2
from google.cloud import vision_v1p4beta1 as vision
from google.cloud import vision
#from google.protobuf.json_format import MessageToDict









@background(schedule=1)  # Check every 1 second
def check_plate_in_database(*args, **kwargs):
    # Initialize the Google Cloud Vision client
    client = vision.ImageAnnotatorClient()
    ser = serial.Serial('/dev/tty/ACM0', 9600)
    def receive_image(width, height):
        
        image_data = ser.read(height*width)
        
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        
        return image_array.reshape((height, width))

    width, height = 320, 240
    
    image = receive_image(width, height)

        # Convert the image array to bytes
    _, image_bytes = cv2.imencode('.jpg', image)

        # Perform text detection using Google Cloud Vision API
    image = vision.Image(content=image_bytes.tobytes())
    response = client.text_detection(image=image)
    texts = response.text_annotations

        # Convert the image bytes back to a NumPy array
    nparr = np.frombuffer(image_bytes, dtype=np.uint8)
    received_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Display the received image with detected text
    cv2.imshow('Received Image', received_image)
    cv2.imwrite('output_image.jpg', received_image)  # Replace 'output_image.jpg' with the desired output path and filename

        # Print extracted text
    if texts:
        for text in texts:
            text.description = ''+ text.description
            if Plate.objects.filter(plates=text.description).exists():
            # Perform some action, e.g., send notification
                
                send_mail(
                'ALERT A MATCHING PLATE FOUND',
                f'The Mtaching Plate : {text.description}',
                'donmukisajoseph@gmail.com',
                ['arindaj33@gmail.com','zbagabo@gmail.com','donjosephmukisa@gmail.com','donmukisajoseph@gmail.com'],
                fail_silently=False,
                )
                print('Email Sent')
                print(text.description)
            
            #print(text.description)
        text.description = ''

    ser.close()
    cv2.destroyAllWindows()


check_plate_in_database()