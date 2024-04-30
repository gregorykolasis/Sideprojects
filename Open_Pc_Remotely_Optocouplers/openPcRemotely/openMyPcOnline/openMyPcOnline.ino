#include <ESP8266WiFi.h>

const char* ssid = <YOUR WIFI NAME>;
const char* password = <YOUR WIFI PASSWORD>;
const char ON = '+', 
 OFF = '-',
 SLEEP = '/',
 AUTO = 'A';


const int pinPowerLightOut = D1,
 pinPowerLightIn = D5,
 pinPowerButton = D6,
 pinResetButton = D7,


 buttonPressTime = 250;


char currentStatus = OFF;
char lightStatus = AUTO;


unsigned long autoDisconnectTime = 0,
 powerButtonReleaseTime = 0;


WiFiServer wifiServer(80);
WiFiClient client;


unsigned long lastOn = 0,
 lastOff = 0;


void changeStatusTo(char newStatus)
{
 if(newStatus != currentStatus)
 {
   Serial.print("Status changed to ");
   Serial.println(newStatus); 
 } 
 currentStatus = newStatus;
}


void recordLightStatusChange(bool lightIn)
{
 if(lightIn)
 lastOn = millis();
 else
 lastOff = millis();


if(lightStatus == AUTO);
 digitalWrite(pinPowerLightOut, lightIn);


}
void statusChange()
{
 bool currentLightStatus = !digitalRead(pinPowerLightIn);


if(lastOn != 0 && lastOff != 0)
 {
 if((millis() < lastOn + 4000) && (millis() < lastOff + 4000))
 {
   changeStatusTo(SLEEP);
   recordLightStatusChange(currentLightStatus);
   return;
 } 
 }


if(currentLightStatus)
 changeStatusTo(ON);
 else
 changeStatusTo(OFF); 


 recordLightStatusChange(currentLightStatus);
}


void Print(String toPrint)
{
 client.print(toPrint);
 Serial.print(toPrint);
}
void Println(String toPrint)
{
 client.println(toPrint);
 Serial.println(toPrint);
}


void processCommand(String command)
{
 Serial.print(F("Received command "));
 Serial.println(command);


if(command.equalsIgnoreCase(F("status")))
 {
 Print("Status: ");
 if(currentStatus == ON)
 Println("On");
 else if(currentStatus == OFF)
 Println("Off");
 else if(currentStatus == SLEEP)
 Println("Sleeping");
 }
 else if(command.equalsIgnoreCase(F("on")))
 {
 if(currentStatus != ON)
 {
 Println("Power Button Pressed (powering on)");
 pressPowerButton(buttonPressTime);
 }
 else
 Println("Machine is already on (button not pressed)");


}
 else if(command.equalsIgnoreCase(F("off")))
 {
 if(currentStatus == ON)
 {
 Println("Power Button Pressed (powering off)");
 pressPowerButton(buttonPressTime);
 }
 else
 Println("Machine is already off (button not pressed)");


}
 else if(command.equalsIgnoreCase(F("reset")))
 {
 unsigned long releaseTime = millis() + 500;
 digitalWrite(pinResetButton, HIGH);
 while(millis() < releaseTime)
 {}
 digitalWrite(pinResetButton, LOW);


Println("Reset Button Pressed");
 }
 else if(command.equalsIgnoreCase(F("force off")))
 {
 if(currentStatus != OFF)
 {
 Print("Holding Power Button for 10 seconds...");
 pressPowerButton(10000);
 }
 }
 else if(command.equalsIgnoreCase(F("pressPwr")))
 {
 digitalWrite(pinPowerButton, HIGH);
 Println("Power Button Pressed");
 }
 else if(command.equalsIgnoreCase(F("releasePwr")))
 {
 digitalWrite(pinPowerButton, LOW);
 Println("Power Button Released");
 }
 else if(command.equalsIgnoreCase(F("light on")))
 {
 setLightStatus(ON);
 }
 else if(command.equalsIgnoreCase(F("light off")))
 {
 setLightStatus(OFF);
 }
 else if(command.equalsIgnoreCase(F("light auto")))
 {
 setLightStatus(AUTO);
 }
}


void setLightStatus(char newStatus)
{
 if(newStatus == ON)
 {
 digitalWrite(pinPowerLightOut, HIGH);
 Println("Light On");
 return; 
 }


 if(newStatus == OFF)
 {
 digitalWrite(pinPowerLightOut, LOW);
 Println("Light Off"); 
 return;
 }


 if(newStatus == AUTO)
 {
 Println("Light Set to Auto"); 
 setLightStatus(currentStatus);
 }


}


void pressPowerButton(int duration)
{
 powerButtonReleaseTime = millis() + (duration);
 digitalWrite(pinPowerButton, HIGH);
}


void runRoutineChecks()
{
 checkIfPowerNeedsToRelease();


if((millis() > lastOn + 4000) && (millis() > lastOff + 4000))
 statusChange();
}


void checkIfPowerNeedsToRelease()
{
 if(powerButtonReleaseTime != 0)
 {
 if(millis() >= powerButtonReleaseTime)
 {
 digitalWrite(pinPowerButton, LOW);
 powerButtonReleaseTime = 0;
 Println("Power Button Released");
 } 
 }
}


/////////////----------------------------------------------------------------------------


void setup() {
 Serial.begin(115200); 
 pinMode(pinPowerLightIn, INPUT_PULLUP);
 pinMode(pinPowerLightOut, OUTPUT);
 pinMode(pinPowerButton, OUTPUT);
 pinMode(pinResetButton, OUTPUT);


 attachInterrupt(digitalPinToInterrupt(pinPowerLightIn), statusChange, CHANGE);


 WiFi.begin(ssid, password);


while (WiFi.status() != WL_CONNECTED)
 {
 delay(1000);
 Serial.println("Connecting..");
 }


Serial.print("Connected to WiFi. IP:");
 Serial.println(WiFi.localIP());


 wifiServer.begin();
}


///////////////////////////////////////////////////////////////////////////////////////////////////


void loop()
{ 


 runRoutineChecks();


 client = wifiServer.available();
 if (client)
 {
 while (client.connected())
 {
 String comm = ""; 
 while (client.available()>0)
 {
 char c = client.read();


autoDisconnectTime = millis() + 60000;


 if(c == ';')
 {
 processCommand(comm);
 comm = "";
 }
 else
 {
 comm.concat(c);
 }
 }
 runRoutineChecks();
 if(autoDisconnectTime > 1000 && millis() > autoDisconnectTime)
 {
 Serial.println("Client timeout"); 
 client.stop();
 }
 }
 client.stop();
 Serial.println("Client disconnected");
 autoDisconnectTime = 0; 
 }
}
