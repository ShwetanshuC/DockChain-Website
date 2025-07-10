

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
// '4': temp 'progress' status: inactive => started => securityCleared => cargoPickedUp => exited
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

std::vector<int> startedJobs = {};

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
}

void loop() {
  
  startedJobs = {};
  
  for (int i = 0; i < (sizeof(jobs) / sizeof(jobs[0])); i++) {
    if (jobs[i][4][0] == "securityCleared") {
      startedJobs.push_back(i);
    }
  }

  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("There are " + String(startedJobs.size()));
  lcd.setCursor(0, 1);
  lcd.print("jobs ready");
  if (startedJobs.size() != 0) {
    delay(1500);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Loading upcoming jobs");
    lcd.setCursor(0, 1);
    lcd.print("by priority...");
  }

  for (int i = 0; i < startedJobs.size(); i++) {
    delay(800);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Job #" + String(jobs[startedJobs[i]][1][1]));
    lcd.setCursor(0, 1);
    lcd.print("Data");

    String driverString = jobs[startedJobs[i]][0][0] + " " + jobs[startedJobs[i]][0][1];
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

    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(jobs[startedJobs[i]][1][0]);
    lcd.setCursor(0, 1);
    lcd.print(jobs[startedJobs[i]][1][1]);

    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Cargo location:");
    lcd.setCursor(0, 1);
    lcd.print(jobs[startedJobs[i]][2][0]);

    delay(1200);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Arrival time:");
    lcd.setCursor(0, 1);
    lcd.print(String(jobs[startedJobs[i]][5][0]) + "AM"); // 
  }

  delay(1200);
  if (startedJobs.size() != 0) {
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
      Serial.println("Success!");
      jobs[startedJobs[0]][4][0] = "cargoPickedUp";
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