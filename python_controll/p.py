import serial
import numpy as np
import cv2

ser = serial.Serial('/dev/ttyACM0', 9600)

def receive_image(width, height):
    image_data = ser.read(width * height)
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    return image_array.reshape((height, width))

def main():
    width, height = 640, 480
    while True:
        image = receive_image(width, height)
        cv2.imshow('Received Image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

ser.close()
cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
