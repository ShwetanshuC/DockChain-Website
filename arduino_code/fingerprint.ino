#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

#include "comparison.h"  // compareHexVectors(vector1, vector2)

#include <vector>

#include <WiFiS3.h>
#include <WifiClient.h>
#include "secrets.h"
#include "ThingSpeak.h"  // always include thingspeak header file after other header files and custom macros

char ssid[] = HIDDEN_SSID;  //  your network SSID (name)
// char pass[] = HIDDEN_PASS;   // your network password
int keyIndex = 0;  // your network key Index number (needed only for WEP)
WiFiClient client;

unsigned long currentChannelNumber = CH_ID_1;
const char* writeAPIKey = WRITE_APIKEY;
const char* readAPIKey = READ_APIKEY;
/*
#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
// For UNO and others without hardware serial, we must use software serial
// ----------------------> pin #2 is IN from sensor (GREEN wire) <----------------------
// ----------------------> pin #3 is OUT from arduino  (WHITE wire) <----------------------
// Set up the serial port to use softwareserial..*/
SoftwareSerial mySerial(6, 7);
/*
#else
// On Leonardo/M0/etc, others with hardware serial, use hardware serial!
// #0 is green wire, #1 is white
#define mySerial Serial1*/


Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup() {
  while (!Serial)
    ;
  Serial.begin(9600);
  Serial.println("Fingerprint template extractor");

  // set the data rate for the sensor serial port
  finger.begin(57600);

  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
    while (1)
      ;
  }

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true)
      ;
  }

  String fv = WiFi.firmwareVersion();
  if (fv != "1.0.0") {
    Serial.println("Please upgrade the firmware");
  }

  ThingSpeak.begin(client);  //Initialize ThingSpeak
}

uint8_t readnumber(void) {
  uint8_t num = 0;

  while (num == 0) {
    while (!Serial.available())
      ;
    num = Serial.parseInt();
  }
  return num;
}

void loop() { /*

  // Connect or reconnect to WiFi
  if(WiFi.status() != WL_CONNECTED){
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(HIDDEN_SSID);
    while(WiFi.status() != WL_CONNECTED){
      WiFi.begin(ssid); // Connect to WPA/WPA2 network. Change this line if using open or WEP network
      Serial.print(".");
      delay(5000);     
    } 
    Serial.println("\nConnected.");
  }
  
  id = 1  // the current fingerprint is always the 1st one
  Serial.print("Enrolling ID #");
  Serial.println(id);

  getFingerprintEnroll();

  // Get template for first fingerprint, which should be the only one
  std::string savePrint = downloadFingerprintTemplate(1);

  // read fingerprint database
   // Read in field 1 of the private channel which is a counter  
  vector<String> fingerData = ThingSpeak.readStringField(currentChannelNumber, 1, readAPIKey);  

   // Check the status of the read operation to see if it was successful
  statusCode = ThingSpeak.getLastReadStatus();
  if(statusCode == 200){
    Serial.println("Counter: " + String(count));
  }
  else{
    Serial.println("Problem reading channel. HTTP error code " + String(statusCode)); 
  }

  // create random fingerprint ID

  int fingerprintID = rand() % 10000000000000000000;

  std::string fingerStringID = std::to_string(fingerprintID);
  fingerStringID.insert(0, 20-(fingerStringID.length()), '0');

  fingerData.push_back(std::to_string({fingerStringID : savePrint}));

  // transmit hex code to Thingspeak database for further storage & identification

  int x = ThingSpeak.writeField(currentChannelNumber, 1, fingerData, writeAPIKey);

  if(x == 200){
    Serial.println("Channel update successful.");
  }
  else{
    Serial.println("Problem updating channel. HTTP error code " + String(x));
  }
  // clear location of fingerprint
  finger.deleteModel(1);
  */
}

uint8_t downloadFingerprintTemplate() {
  int id = 1;
  Serial.println("------------------------------------");
  Serial.print("Attempting to load #");
  Serial.println(1);
  uint8_t p = finger.loadModel(1);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.print("Template ");
      Serial.print(1);
      Serial.println(" loaded");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    default:
      Serial.print("Unknown error ");
      Serial.println(p);
      return p;
  }

  // OK success!

  Serial.print("Attempting to get #");
  Serial.println(1);
  p = finger.getModel();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.print("Template ");
      Serial.print(1);
      Serial.println(" transferring:");
      break;
    default:
      Serial.print("Unknown error ");
      Serial.println(p);
      return p;
  }

  // one data packet is 267 bytes. in one data packet, 11 bytes are 'usesless' :D
  uint8_t bytesReceived[534];  // 2 data packets
  memset(bytesReceived, 0xff, 534);

  uint32_t starttime = millis();
  int i = 0;
  while (i < 534 && (millis() - starttime) < 20000) {
    if (mySerial.available()) {
      bytesReceived[i++] = mySerial.read();
    }
  }
  Serial.print(i);
  Serial.println(" bytes read.");
  Serial.println("Decoding packet...");

  uint8_t fingerTemplate[512];  // the real template
  memset(fingerTemplate, 0xff, 512);

  // filtering only the data packets
  int uindx = 9, index = 0;
  memcpy(fingerTemplate + index, bytesReceived + uindx, 256);  // first 256 bytes
  uindx += 256;                                                // skip data
  uindx += 2;                                                  // skip checksum
  uindx += 9;                                                  // skip next header
  index += 256;                                                // advance pointer
  memcpy(fingerTemplate + index, bytesReceived + uindx, 256);  // second 256 bytes

  std::vector<std::string> hexver;
  for (int i = 0; i < 512; ++i) {
    //Serial.print("0x");
    hexver.push_back(getHex(fingerTemplate[i], 2));
    //Serial.print(", ");
  }

  //Serial.print(hexver);            <-----------------------

  /*
    uint8_t templateBuffer[256];
    memset(templateBuffer, 0xff, 256);  //zero out template buffer
    int index=0;
    uint32_t starttime = millis();
    while ((index < 256) && ((millis() - starttime) < 1000))
    {
    if (mySerial.available())
    {
      templateBuffer[index] = mySerial.read();
      index++;
    }
    }

    Serial.print(index); Serial.println(" bytes read");

    //dump entire templateBuffer.  This prints out 16 lines of 16 bytes
    for (int count= 0; count < 16; count++)
    {
    for (int i = 0; i < 16; i++)
    {
      Serial.print("0x");
      Serial.print(templateBuffer[count*16+i], HEX);
      Serial.print(", ");
    }
    Serial.println();
    }*/
}

std::string getHex(int num, int precision) {
  char tmp[16];
  char format[128];

  sprintf(format, "%%.%dX", precision);

  sprintf(tmp, format, num);
  return tmp;
}

uint8_t getFingerprintEnroll() {

  int p = -1;
  Serial.print("Waiting for valid finger to enroll as #");
  Serial.println(1);
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        Serial.println("Image taken");
        break;
      case FINGERPRINT_NOFINGER:
        Serial.print(".");
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("Imaging error");
        break;
      default:
        Serial.println("Unknown error");
        break;
    }
  }

  // OK success!

  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  Serial.println("Remove finger");
  delay(2000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }
  Serial.print("ID ");
  Serial.println(1);
  p = -1;
  Serial.println("Place same finger again");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        Serial.println("Image taken");
        break;
      case FINGERPRINT_NOFINGER:
        Serial.print(".");
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("Imaging error");
        break;
      default:
        Serial.println("Unknown error");
        break;
    }
  }

  // OK success!

  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  Serial.print("Creating model for #");
  Serial.println(1);

  p = finger.createModel();
  if (p == FINGERPRINT_OK) {
    Serial.println("Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    Serial.println("Fingerprints did not match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  Serial.print("ID ");
  Serial.println(1);
  p = finger.storeModel(1);
  if (p == FINGERPRINT_OK) {
    Serial.println("Stored!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("Could not store in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("Error writing to flash");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  return true;
}
