import serial
import numpy as np
import cv2
from google.cloud import vision_v1p4beta1 as vision
from google.protobuf.json_format import MessageToDict

# Initialize the Google Cloud Vision client
client = vision.ImageAnnotatorClient()

ser = serial.Serial('COM1', 115200)

def receive_image(width, height):
    image_data = ser.read(width * height)
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

def main():
    width, height = 640, 480
    while True:
        image = receive_image(width, height)

        # Perform object detection and label extraction
        object_labels = detect_objects(image)

        # Convert the image array back to an image
        received_image = np.array(image, dtype=np.uint8)

        # Display the received image
        cv2.imshow('Received Image', received_image)

        # Print detected object labels
        if object_labels:
            print('Detected Objects:', ', '.join(object_labels))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ser.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
