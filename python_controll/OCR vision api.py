 
import serial
import numpy as np
import cv2
from google.cloud import vision_v1p4beta1 as vision

# Initialize the Google Cloud Vision client
client = vision.ImageAnnotatorClient()

ser = serial.Serial('COM1', 9600)

def receive_image(width, height):
    image_data = ser.read(width * height)
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    return image_array.reshape((height, width))

def detect_number_plates(image):
    # Convert the image array to bytes
    _, image_bytes = cv2.imencode('.jpg', image)

    # Perform text detection using Google Cloud Vision API
    image = vision.Image(content=image_bytes.tobytes())
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Extract number plate text (if available)
    number_plate_text = None
    if texts:
        number_plate_text = texts[0].description

    return number_plate_text

def main():
    width, height = 640, 480
    while True:
        image = receive_image(width, height)

        # Perform number plate detection and text extraction
        number_plate_text = detect_number_plates(image)

        # Convert the image array back to an image
        received_image = np.array(image, dtype=np.uint8)

        # Display the received image
        cv2.imshow('Received Image', received_image)

        # Print extracted number plate text
        if number_plate_text:
            print('Number Plate Text:', number_plate_text)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ser.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

