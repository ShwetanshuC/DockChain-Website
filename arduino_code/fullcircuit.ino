// THIS CODE SHOULD CONNECT TO COM9

#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <Servo.h>
#include <WiFiS3.h>
#include "fingerprintFunctions.h"

#include <vector>

#include "ThingSpeak.h"  // always include thingspeak header file after other header files and custom macros

#define HOST "localhost"
#define WIFI_SSID "DESKTOP-QH1UG56 5470" // "Leon's iPhone"
#define WIFI_PASSWORD "26P[45r9"// "esay2023"

#define CH_ID_1 3004321  // replace 0000000 with your channel number
#define WRITE_APIKEY "RLZVGP2KW5T7SNFW"
#define READ_APIKEY "AS81JAIZZDWQWWUS"

// assigning digital pin values for LED and servo

int servoPin = 9;

int redPin = 12;
int greenPin = 11;

// list of license plates - purely for testing purposes

std::vector<String> licensePlates = { "2W96", "FG18", "J73K", "DLUYW", "Q32E" };

int plateSelectionInit = 0;
int plateSelectionFinal = 0;

// hypothetical list of jobs - also for testing purposes
// 0: trucker object
// 0: trucker first name
// 1: trucker last name
// 2: role
// 3: date posted
// 1: license plate object
// 0: state
// 1: plate number
// 2: date added
// '2': cargo id number
// '3': temp fingerprint id
// '4': temp 'progress' status: inactive => started => securityCleared => cargoPickedUp => exited
/* std::vector<std::vector<std::vector<String>>> jobs = {
  { { "CEO", "Shwetanshu", "Goon", "07/08/25" },
    { "North Carolina", "2W96", "07/08/25" },
    { "A5" },
    { "" },
    { "started" } },
  { { "Retard", "Aadarsh", "Auramaxxer", "07/08/25" },
    { "North Carolina", "FG18", "07/08/25" },
    { "B2" },
    { "" },
    { "started" } },
  { { "Oh yeah", "Jason", "Trucker", "07/08/25" },
    { "North Carolina", "J73K", "07/08/25" },
    { "C7" },
    { "" },
    { "inactive" } }
};*/

#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
// For UNO and others without hardware serial, we must use software serial...
// pin #2 is IN from sensor (GREEN wire)
// pin #3 is OUT from arduino  (WHITE wire)
// Set up the serial port to use softwareserial..
SoftwareSerial mySerial(2, 3);

#else
// On Leonardo/M0/etc, others with hardware serial, use hardware serial!
// #0 is green wire, #1 is white
#define mySerial Serial1

#endif

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

Servo myServo;

JsonDocument jobDoc;
JsonDocument plateDoc;
JsonDocument initDoc;
JsonDocument finalDoc;

int status = WL_IDLE_STATUS;
WiFiClient client;

String server = "192.168.137.1";
int port = 8000;

void setup() {
  // fingerprint sensor preparation
  finger.emptyDatabase();

  Serial.begin(9600);

  delay(100);

  Serial.println("\n\n\n\n\n\nFull Circuit?");

  // set the data rate for the sensor serial port
  finger.begin(57600);

  delay(100);

  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  }
  else {
    Serial.println("Did not find fingerprint sensor :(");
  }

  Serial.println(F("Reading sensor parameters"));
  finger.getParameters();
  Serial.print(F("Status: 0x")); Serial.println(finger.status_reg, HEX);
  Serial.print(F("Sys ID: 0x")); Serial.println(finger.system_id, HEX);
  Serial.print(F("Capacity: ")); Serial.println(finger.capacity);
  Serial.print(F("Security level: ")); Serial.println(finger.security_level);
  Serial.print(F("Device address: ")); Serial.println(finger.device_addr, HEX);
  Serial.print(F("Packet len: ")); Serial.println(finger.packet_len);
  Serial.print(F("Baud rate: ")); Serial.println(finger.baud_rate);
  
  // LED preparation

  pinMode(redPin,  OUTPUT);              
  pinMode(greenPin, OUTPUT);

  setColor("none");

  // servo motor prep

  myServo.attach(servoPin);

  myServo.write(90);
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }


  // wifi connection
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(WIFI_SSID);

    if (WIFI_PASSWORD =="") {
    status = WiFi.begin(WIFI_SSID); // WIFI_SSID
    }
    else {
      status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    }
    // wait 10 seconds for connection:
    delay(10000);
  }

  //client.setCACert(test_root_ca);
  //printWifiStatus();
  //testConnection();
}

// just as a note, one "loop" is one entrance/exit pair
void loop() {
  // String host_ip = "http://172.27.24.130:8000/truckmanagement/arduino"; //check filepath
  // request all job info

  String jobs = getData("value=active_jobs&job_id=0");
  Serial.println("String for jobs:" + jobs);
  DeserializationError error = deserializeJson(jobDoc, jobs);
  // clear all fingerprints

  int w = finger.emptyDatabase();
  if (w != FINGERPRINT_OK) {
    Serial.println("Error occured when emptying database: " + String(w));
  }

  w = finger.getTemplateCount();
  if (w != FINGERPRINT_OK) {
    Serial.println("Error occured when getting template count: " + String(w));
  }

  // get entering license plate from some list
  String initialPlate = getData("value=plate_initial&job_id=0"); // licensePlates[plateSelectionInit];
  Serial.println("String for initial plate:" + initialPlate);
  error = deserializeJson(initDoc, initialPlate);

  String allPlates = getData("value=plates_all&job_id=0");
  Serial.println("String for plates:" + allPlates);
  error = deserializeJson(plateDoc, allPlates);
  // select correct job based on license plate - this is currently susceptible to license plate multi-use

  int currentJob = -1;

  for (int i = 0; i < jobDoc.size(); i++) {        
    String correspondingPlate = findPlate(jobDoc[i]["license_plate_id"]);
    if (correspondingPlate != "") {                 /// this should be doc reference
      Serial.println("Checking job #" + String(i+1) + ", comparing " + correspondingPlate + " to " + String(initDoc["plate"]));
      // this should be doc reference
      if (correspondingPlate == String(initDoc["plate"])) {
        currentJob = int(jobDoc[i]["id"]);
        break;
      }
    }
  }

  if (currentJob == -1) {
    Serial.println("Plate not found!");
    return;
  }

  // checking capacity of fingerprint sensor
  int p = finger.getTemplateCount();
  if (p != FINGERPRINT_OK) {
    Serial.println("Communication error occured when getting template count!");
  }

  int nextID = finger.templateCount + 1;

  // get fingerprint from fingerprint sensor + id

  int r = 10;
  while (r==10) {
    r = getFingerprintEnroll(nextID, finger, true);
    Serial.println("Return code: " + String(r));
  }

  // transmit fingerprint ID to 'mysql database' utilizing found job
  String result;
  result = sendData(currentJob, "print_id", String(nextID)); //jobs[currentJob][3][0] = String(nextID);
  result = sendData(currentJob, "status", "SecurityCleared"); //jobs[currentJob][4][0] = "securityCleared";
  // ... handle errors
  // this is probably part of the above step, but send "security cleared" indicator to job on mysql database

  // light up led - you can add error detection later
  for(int y=0;y<3;y++) {
    setColor("red");
    delay(200);
    setColor("none");
    delay(200);
  }

  myServo.write(90);
  delay(12000);
  String check;
  while (true) {
    // checking if cargo cleared signal has been sent
    check = getData("value=status&job_id=" + String(currentJob));
    if (check=="CargoPickedUp") {
      break;
    }
  }

  // get returning license plate from some list or from an image (?)

  String exitPlate = getData("value=plate_final&job_id=0");//licensePlates[plateSelectionFinal];
  error = deserializeJson(finalDoc, exitPlate);
  // compare initial and returning license plate, only continue if they match
                  // this should be doc reference
  if (finalDoc["plate"] != initDoc["plate"]) {
    sendError("Plates do NOT match!");
    while (1) {};
  }


  // get previous fingerprint ID
  int prevID = (getData("value=temp_finger&job_id=" + String(currentJob))).toInt();

  p = finger.getTemplateCount();
  if (p != FINGERPRINT_OK) {
    Serial.println("Communication error occured when getting template count!");
  }

  nextID = finger.templateCount + 1;

  // get fingerprint from fingerprint sensor

  getFingerprintEnroll(nextID, finger, false);

  // utilize compare function located on fingerprint sensor to compare entering fingerprint with final fingerprint
  std::vector<float> results = compareFingerprint(prevID, finger);

  std::vector<float> commerror = {0, 0, 0};
  std::vector<float> notfound = {1, 1, 1};

  if (results == commerror) {
    sendError("Communication error upon comparing fingerprints!");
    return;
  } else if (results == notfound) {
    sendError("Exit fingerprint not found within database!");
    return;
  } else {
    // if confidence score is less than some threshhold, do not continue (have function for this)
    Serial.println("Results: " + String(results[0]) + ", " + String(results[1]) + ", " + String(results[2]));
    if (results[2] <55) {
      sendError("Fingerprint match confidence below required threshhold. Confidence = " + String(results[2]));
      while (1) {};
    }

    // light up led

    setColor("red");

    delay(1000);

    // turn servo motor
    myServo.write(0);

    delay(10000);

    myServo.write(90);
    setColor("none");

    result = sendData(currentJob, "status", "Completed"); // check status name
  }
}

void sendError(String message) {
  Serial.println(message);
  setColor("red"); 
  delay(3000);
  setColor("none");
}

void setColor(String directive) {
  if (directive == "red") {
    digitalWrite(redPin, HIGH);
  }
  else if (directive == "green") {
    digitalWrite(greenPin,  HIGH);
  }
  else {
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, LOW);
  }
}

String getData(String path) {
  String urlWithData = "/truckmanagement/arduino_endpoint/?" + path;
  String response = "";
  
  if (client.connect(server.c_str(), port)) {
    // Send HTTP request
    client.println("GET " + urlWithData + " HTTP/1.1");
    client.println("Host: " + server + ":" + String(port));
    //client.println("User-Agent: Arduino/1.0");
    client.println("Connection: close");
    client.println();
    
    // Wait for response
    unsigned long timeout = millis();
    while (client.available() == 0) {
      if (millis() - timeout > 20000) {
        Serial.println("Client timeout!");
        client.stop();
        return "TIMEOUT";
      }
    }
    
    // Read response
    bool headersEnded = false;
    String line;
    
    while (client.available()) {
      line = client.readStringUntil('\n');
      
      // Skip headers, only capture body
      if (headersEnded) {
        response += line + "\n";
      }
      
      // Check if we've reached the end of headers
      if (line.length() == 1 && line.charAt(0) == '\r') {
        headersEnded = true;
      }
    }
    
    client.stop();
  } else {
    return "CONNECTION_FAILED";
  }
  
  return response;
}

String sendData(int job_id, String column, String message) {
  String requestBody = "job_id=" + String(job_id) + "&column=" + column + "&message=" + message;
  String path = "/truckmanagement/arduino_endpoint/";
  Serial.print("Sending data: ");
  Serial.println("job #" + String(job_id) + ", column " + column + ", value " + message);

  String response = "";

  if(client.connect(server.c_str(), port)) {
    client.println("POST " + path + " HTTP/1.1");
    client.println("Host: " + server + ":" + String(port));
    //client.println("User-Agent: Arduino/1.0");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Content-Length: " + String(requestBody.length()));
    client.println("Connection: close");
    client.println();
    client.println(requestBody);
    // Wait for response
    unsigned long timeout = millis();
    while (client.available() == 0) {
      if (millis() - timeout > 20000) {
        Serial.println("Client timeout!");
        client.stop();
        return "TIMEOUT";
      }
    }
    
    // Read response
    bool headersEnded = false;
    String line;
    
    while (client.available()) {
      line = client.readStringUntil('\n');
      
      // Skip headers, only capture body
      if (headersEnded) {
        response += line + "\n";
      }
      
      // Check if we've reached the end of headers
      if (line.length() == 1 && line.charAt(0) == '\r') {
        headersEnded = true;
      }
    }
    
    client.stop();
  } else {
    return "CONNECTION_FAILED";
  }
}

void printWifiStatus() { 
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
/*
void read_response() { 
  uint32_t received_data_num = 0;
  while (client.available()) {
    // actual data reception 
    char c = client.read();
    // print data to serial port 
    Serial.print(c);
    // wrap data to 80 column
    received_data_num++;
    if(received_data_num % 80 == 0) { 
      Serial.println();
    }
  }  
}*/

void testConnection() {
  Serial.println("Testing basic connectivity...");
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected");
    Serial.print("Arduino IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("Gateway IP: ");
    Serial.println(WiFi.gatewayIP());
  } else {
    Serial.println("WiFi not connected!");
    return;
  }
  
  // Test basic HTTP connection
  Serial.println("Attempting HTTP connection...");
  
  String server = "192.168.137.1";
  int port = 8000;
  String path = "/";
  
  if (client.connect(server.c_str(), port)) {
    Serial.println("Connected to server");
    
    // Make HTTP GET request
    client.println("GET " + path + " HTTP/1.1");
    client.println("Host: " + server + ":" + String(port));
    client.println("User-Agent: Arduino/1.0");
    client.println("Connection: close");
    client.println(); // Empty line to end headers
    
    // Wait for response
    unsigned long timeout = millis();
    while (client.available() == 0) {
      if (millis() - timeout > 20000) {
        Serial.println("Client timeout!");
        client.stop();
        return;
      }
    }
    
    // Read response
    Serial.println("HTTP Response:");
    Serial.println("==============");
    
    bool headersEnded = false;
    String line;
    
    while (client.available()) {
      line = client.readStringUntil('\n');
      Serial.println(line);
      
      // Check if we've reached the end of headers
      if (line.length() == 1 && line.charAt(0) == '\r') {
        headersEnded = true;
      }
    }
    
    client.stop();
    Serial.println("==============");
    Serial.println("Connection closed");
    
  } else {
    Serial.println("Connection failed");
  }
}

String findPlate(int plate_id) {
  for (int i=0;i<plateDoc.size();i++) {
    if (plateDoc[i]["id"] == plate_id) {
      return plateDoc[i]["plate_number"];
    }
  }
  return "";
}

int findJob(int job_id) {
  for (int i=0;i<jobDoc.size();i++) {
    if (jobDoc[i]["id"] == job_id) {
      return i;
    }
  }
  return -1;
}
