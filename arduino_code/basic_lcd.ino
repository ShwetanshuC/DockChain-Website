

// side note: lcd.print is (column, row)


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
// '4': temp 'progress' status: Pending => Approved/Denied => Started => SecurityCleared => CargoPickedUp => Exited
// '5': time of recent interaction (i.e. passing security, picking up cargo)

/*
std::vector<std::vector<std::vector<String>>> jobs = {
  { { "Jobless", "Shwetanshu", "Goon", "07/08/25" },
    { "North Carolina", "2W96", "07/08/25" },
    { "A5-32" },
    { "" },
    { "securityCleared" },
    { "10" } },
  { { "Matchadrinking", "Aadarsh", "Auramaxxer", "07/08/25" },
    { "North Carolina", "FG18", "07/08/25" },
    { "B2-21" },
    { "" },
    { "started" },
    { "7" } },
  { { "Locked In", "Jason", "Trucker", "07/08/25" },
    { "North Carolina", "J73K", "07/08/25" },
    { "C7-18" },
    { "" },
    { "inactive" },
    { "8" } }
};

std::vector<std::vector<std::vector<String>>> startedJobs = {};

std::vector<std::vector<String>> startedJobIDs = {}; 
*/

// Libraries to include
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <DHT22.h>
#include <vector>

#include <R4HttpClient.h>

#include "ThingSpeak.h"  // always include thingspeak header file after other header files and custom macros

#define HOST "localhost"
#define WIFI_SSID "DESKTOP-QH1UG56 5470" // "Leon's iPhone"
#define WIFI_PASSWORD "26P[45r9"// "esay2023"

JsonDocument jobDoc;
JsonDocument driverDoc;
JsonDocument licenseDoc;

int status = WL_IDLE_STATUS;
WiFiSSLClient client;
R4HttpClient http;

char server[] = "127.0.0.1";

// sorting of database will be done by Shwet's python code
// std::vector<std::vector<std::vector<String>>
String jobs[3][6][4] = {
  { { "Jobless", "Shwetanshu", "Goon", "07/08/25" },
    { "North Carolina", "2W96", "07/08/25", "" },
    { "A5-32", "", "", "" },
    { "", "", "", "" },
    { "securityCleared", "", "", "" },
    { "10", "", "", "" } },
  { { "Matchadrinking", "Aadarsh", "Auramaxxer", "07/08/25" },
    { "North Carolina", "FG18", "07/08/25" },
    { "B2-21", "", "", "" },
    { "", "", "", "" },
    { "started", "", "", "" },
    { "7", "", "", "" } },
  { { "Locked In", "Jason", "Trucker", "07/08/25" },
    { "North Carolina", "J73K", "07/08/25" },
    { "C7-18", "", "", "" },
    { "", "", "", "" },
    { "inactive", "", "", "" },
    { "8", "", "", "" } }
};


// init LCD with interface pins
LiquidCrystal_I2C lcd(0x27, 16, 2);

int buttonPin = 2;

void setup() {
  Serial.begin(9600);
  // initialize button pin to recieve job completion signal
  pinMode(buttonPin, INPUT_PULLUP);

  lcd.init();  // Initializes LCD display
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Welcome to");  // Welcomes user to interface
  lcd.setCursor(0, 1);
  lcd.print("DockChain!");
  delay(3000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Preparing jobs..");  // Welcomes user to interface

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
  printWifiStatus();
}

void loop() {

  String server = "192.168.137.1";
  int port = 8000;
  // request all job info

  String startedJobs = getData("value=securedJobs");
  
  DeserializationError error = deserializeJson(jobDoc, startedJobs);
  if (error) {
    Serial.println("Error when deserializing JSON and writing to doc: " + String(error))
  }

  drivers = getData("value=drivers");
  
  DeserializationError error = deserializeJson(driverDoc, drivers);
  if (error) {
    Serial.println("Error when deserializing JSON and writing to doc: " + String(error))
  }
  
  plates = getData("value=plates_all");
  
  DeserializationError error = deserializeJson(licenseDoc, plates);
  if (error) {
    Serial.println("Error when deserializing JSON and writing to doc: " + String(error))
  }
  
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("There are " + String(jobDoc.size()));
  lcd.setCursor(0, 1);
  lcd.print("jobs ready");
  if (jobDoc.size() != 0) {
    delay(1500);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Loading upcoming jobs");
    lcd.setCursor(0, 1);
    lcd.print("by priority...");
  }
                      // this should be doc reference
  for (int i = 0; i < jobDoc.size(); i++) {
    delay(800);
    lcd.clear();
    lcd.setCursor(0, 0); // this should be doc reference
    lcd.print("Job #" + String(jobDoc[i]["id"]));
    lcd.setCursor(0, 1);
    lcd.print("Data");
                        // this should be doc reference
    String driverString = findDriver(jobDoc[i]["driver_id"])
    if (driverString.length() > 16) {
      driverString = driverString.substring(0, 15) + ".";
    }
    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Driver: ");
    lcd.setCursor(0, 1);
    lcd.print(driverString);

    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("LP state");
    lcd.setCursor(0, 1);
    lcd.print("and number:");

    String plateString[] = findPlate(jobDoc[i]["license_plate_id"])

    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(plateString[0]); // this should be doc reference
    lcd.setCursor(0, 1);
    lcd.print(plateString[1]); // this should be doc reference

    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Cargo location:");
    lcd.setCursor(0, 1); // this should be doc reference
    lcd.print(jobDoc[i]["docking_location"]);

    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Arrival time:");
    lcd.setCursor(0, 1); // this should be doc reference
    lcd.print(String(jobDoc[i]["target_timestamp"]) + "AM"); // 
  }

  delay(1200);
  if (jobDoc.size() != 0) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Press button to");
    lcd.setCursor(0, 1);
    lcd.print("finish top job");

    int buttonState = LOW;

    // Define the time limit (e.g., 5 seconds)
    unsigned long time_limit = 5000;

      // Record the start time
    unsigned long start_time = millis();

    while (buttonState == LOW) {
      buttonState = digitalRead(buttonPin);
      unsigned long current_time = millis();

      // Calculate the elapsed time
      unsigned long elapsed_time = (current_time - start_time);

      // Check if the time limit has been exceeded
      if (elapsed_time >= time_limit) {
          break;
      }
    }

    if (buttonState == HIGH) {
      Serial.println("Success!");          // this should be job doc
      result = sendData(String(jobDoc[0]["id"]), "status", "CargoPickedUp");
      //jobs[startedJobs[0]][4][0] = "cargoPickedUp";
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Success!");
      delay(2000);
    }
    else if (buttonState == LOW) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Job finish");
      lcd.setCursor(0, 1);
      lcd.print("bypassed.");
    }
  }
}

uint8_t readnumber(void) {
  uint8_t num = 0;

  while (num == 0) {
    while (! Serial.available());
    num = Serial.parseInt();
  }
  return num;
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
      if (millis() - timeout > 5000) {
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
      if (millis() - timeout > 5000) {
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

String findDriver(int driver_id) {
  for (int i=0;i<driverDoc.size();i++) {
    if (driverDoc[i]["id"] == job_id) {
      return driverDoc[i]["firstname"] + " " + driverDoc[i]["lastname"];
    }
  }
  return "";
}


String[] findPlate(int plate_id) {
  for (int i=0;i<plateDoc.size();i++) {
    if (plateDoc[i]["id"] == plate_id) {
      return [plateDoc[i]["state"], plateDoc[i]["plate_number"]];
    }
  }
  return "";
}
