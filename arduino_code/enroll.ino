#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(6, 7);  // RX, TX
Adafruit_Fingerprint finger(&mySerial);

void setup() {
  Serial.begin(9600);
  while (!Serial); delay(100);
  Serial.println("Initializing sensor...");

  finger.begin(57600);  // Try 9600 if this fails
  if (finger.verifyPassword()) {
    Serial.println("Fingerprint sensor found!");
  } else {
    Serial.println("Could not find fingerprint sensor :(");
    while (1) { delay(1); }
  }
}

void loop() {
  // Nothing here for now
}
