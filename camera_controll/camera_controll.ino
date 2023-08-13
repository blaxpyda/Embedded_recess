#include <TinyMLShield.h>

byte image[320*240];
int bytesPerFrame;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  initializeShield();

  if (!Camera.begin(QVGA, GRAYSCALE, 1, OV7675)) {
    Serial.println("Failed to initialize camera");
    while (1);
  }
  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel();
  
  Serial.println("Raw image data will begin streaming...");
}

void loop() {
  Camera.readFrame(image);
  Serial.write(image, bytesPerFrame); // Send live image data
}
