# platesapp/tasks.py
from background_task import background
from platesapp.models import Plate
from django.core.mail import send_mail
from .models import Plate

#------------------------------------------------------------------------------
import serial
import numpy as np
import cv2
from google.cloud import vision_v1p4beta1 as vision
#from google.protobuf.json_format import MessageToDict









@background(schedule=1)  # Check every 1 second
def check_plate_in_database(*args, **kwargs):
    # Initialize the Google Cloud Vision client
    client = vision.ImageAnnotatorClient()
    ser = serial.Serial('COM5', 9600)
    def receive_image(width, height):
        
        image_data = ser.read(height*width)
        
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        
        return image_array.reshape((height, width))

    def detect_objects(image):
        # Convert the image array to bytes
        _, image_bytes = cv2.imencode('.jpg', image)

        # Perform object detection using Google Cloud Vision API
        image = vision.Image(content=image_bytes.tobytes())
        response = client.object_localization(image=image)
        objects = response.localized_object_annotations

        # Extract object labels (if available)
        object_labels = []
        for obj in objects:
            object_labels.append(obj.name)

        return object_labels

    print('00000000000000000000000000000000000000000000000000000000')
    width, height = 320, 240

    image = receive_image(width, height)

        # Perform object detection and label extraction
    object_labels = detect_objects(image)

        # Convert the image array back to an image
    received_image = np.array(image, dtype=np.uint8)

        # Display the received image
    cv2.imshow('Received Image', received_image)
    cv2.imwrite('output_image.jpg', received_image)  # Replace 'output_image.jpg' with the desired output path and filename

        # Print detected object labels
    if object_labels:
            print('Detected Objects:', ', '.join(object_labels))
    print('111111111111111111111111111111111111111111111111111111111111111')
    
    ser.close()
    cv2.destroyAllWindows()
    
    for label in object_labels:
        print('2222222222222222222222222222222222222222222222222222222222222')
        if Plate.objects.filter(plates=label).exists():
            # Perform some action, e.g., send notification
            print('33333333333333333333333333333333333333333333333333333333333333')
            send_mail(
            'ALERT MATCHING PLATE FOUND',
            f'The Mtaching Plate : {label}',
            'donmukisajoseph@gmail.com',
            ['arindaj33@gmail.com','zbagabo@gmail.com','donjosephmukisa@gmail.com','donmukisajoseph@gmail.com'],
            fail_silently=False,
        )
            print('Email Sent')
            print(label)
            
