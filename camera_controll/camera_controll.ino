/*
####################################################MODIFIED#####################################################################
  OV767X - Camera Capture Raw Bytes and Send to PC

  This sketch reads a frame from the OmniVision OV7670 camera
  and sends the bytes to the PC via serial communication.

  Circuit:
    - Arduino Uno or similar board
    - OV7670 camera module: (connections as mentioned in the original code)

  This example code is in the public domain.
*/

#include <Arduino_OV767X.h>

int bytesPerFrame;

byte data[320 * 240 * 2]; // QVGA: 320x240 X 2 bytes per pixel (RGB565)

void setup() {
  //Serial.begin(115200); // Baud rate for serial communication
  Serial.begin(9600);
  while (!Serial);

  if (!Camera.begin(QVGA, GRAYSCALE, 1)) {
    Serial.println("Failed to initialize camera!");
    while (1);
  }

  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel();

  // Optionally, enable the test pattern for testing
  // Camera.testPattern();
}

void loop() {
  Camera.readFrame(data);

  Serial.write(data, bytesPerFrame);
}
