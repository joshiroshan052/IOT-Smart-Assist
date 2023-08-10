#include <Blynk.h>

#include <dummy.h>

/*New blynk app project
   Home Page
*/

//Include the library files
#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

#define BLYNK_AUTH_TOKEN "sXc5NeI9FfeY-KMPUuEfJY0ThIsPGTkE" //Enter your blynk auth token

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "STW_CU";//Enter your WIFI name
char pass[] = "cov3ntry123";//Enter your WIFI password

//Get the button value
BLYNK_WRITE(V0) {
  digitalWrite(D8, param.asInt());
}

void setup() {
  //Set the LED pin as an output pin
  pinMode(D8, OUTPUT);
  //Initialize the Blynk library
  Blynk.begin(auth, ssid, pass, "blynk.cloud", 80);
}

void loop() {
  //Run the Blynk library
  Blynk.run();
}
