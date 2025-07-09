#include SoftwareSerial

#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

#include "fingerprintFunctions.h"

#include <vector>

#include <WiFiS3.h>
#include <WifiClient.h>
#include "secrets.h"
#include "ThingSpeak.h"  // always include thingspeak header file after other header files and custom macros


#define HIDDEN_SSID "seahawkguest"		// replace MySSID with your WiFi network name
#define HIDDEN_PASS "none"	// replace MyPassword with your WiFi password

#define CH_ID_1 3004321			// replace 0000000 with your channel number
#define WRITE_APIKEY "RLZVGP2KW5T7SNFW"   
#define READ_APIKEY "AS81JAIZZDWQWWUS"  

// assigning digital pin values for LED and servo

int ledPin = 7;

int servoPin = 9;

// list of license plates - purely for testing purposes

std::vector<String> licensePlates = {"2W96", "FG18", "J73K", "DLUYW", "Q32E"};

int plateSelectionInit = 0;
int plateSelectionFinal = 0;

// hypothetical list of jobs - also for testing purposes

SoftwareSerial mySerial(2, 3);

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup() {
  // fingerprint sensor preparation

  Serial.begin(9600);

  delay(1000)

  // set the data rate for the sensor serial port
  finger.begin(57600);

  delay(1000)
  
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
  }
  // LED preparation

  pinMode(ledPin, OUTPUT); 

  // servo motor prep

  pinMode(servoPin, OUTPUT); 

}

// just as a note, one "loop" is one entrance/exit pair
void loop() {

  // get entering license plate from some list

  String initialPlate = licensePlates[plateSelectionInit];

  // get all running jobs from mysql database

  // select correct job based on license plate

  // get fingerprint from fingerprint sensor + id

  // transmit fingerprint ID to mysql database utilizing found job

  // this is probably part of the above step, but send "security cleared" indicator to job on mysql database

  // light up led - you can add error detection later

  // loop to wait for "cargo cleared" signal from job on mysql database, which other arduino would indicate


  // get returning license plate from some list

  // get initial license plate + from mysql database

  // compare initial and returning license plate, only continue if they match

  // get fingerprint from fingerprint sensor

  // utilize compare function located on fingerprint sensor to compare entering fingerprint with final fingerprint

    // if confidence score is less than some threshhold, do not continue (have function for this)

  // light up led

  // turn servo motor


}
