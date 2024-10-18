
/* 
 DESCRIPTION
 ====================
 Simple example of the Bounce library that switches the debug LED when a button is pressed.
 */
// Include the Bounce2 library found here :
// https://github.com/thomasfredericks/Bounce2
#include <Bounce2.h>
#include <Wire.h> 
#include <SPI.h>
#include <Ethernet.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

byte mac[] = { 0xFE, 0xE7, 0xDE, 0xB0, 0xDC, 0x9B };
IPAddress ip(192, 168, 100, 30);//241
IPAddress gateway(192, 168, 100, 254);
IPAddress subnet(255, 255, 255, 0);
IPAddress server(192, 168, 100, 22);

char serverName[] = "192.168.100.22";
int serverPort = 14999;

EthernetServer myserver(9639);
EthernetClient client;
int totalCount = 0;
char pageAdd[64];
bool readyState = false;
unsigned long Timeout = 5000;
int statusCODE = 0;






#define in1Pin 22
#define in2Pin 24
#define in3Pin 26 
#define in4Pin 28
#define in5Pin 30
#define in6Pin 32
#define in7Pin 34
#define in8Pin 36
#define in9Pin 38
#define in10Pin 40
#define in11Pin 42
#define in12Pin 44
#define in13Pin 46
#define in14Pin 48
#define in15Pin 65
#define in16Pin 64
#define in17Pin 63
#define in18Pin 62
#define in19Pin 61
#define in20Pin 60
#define in21Pin 59
#define in22Pin 58
#define in23Pin 57
#define in24Pin 56
#define in25Pin 55
#define in26Pin 54
#define testPin 13

// Instantiate a Bounce object
Bounce in1 = Bounce(); 
Bounce in2 = Bounce(); 
Bounce in3 = Bounce(); 
Bounce in4 = Bounce(); 
Bounce in5 = Bounce(); 
Bounce in6 = Bounce(); 
Bounce in7 = Bounce(); 
Bounce in8 = Bounce(); 
Bounce in9 = Bounce(); 
Bounce in10 = Bounce(); 
Bounce in11 = Bounce(); 
Bounce in12 = Bounce(); 
Bounce in13 = Bounce(); 
Bounce in14 = Bounce(); 
Bounce in15 = Bounce(); 
Bounce in16 = Bounce(); 
Bounce in17 = Bounce(); 
Bounce in18 = Bounce(); 
Bounce in19 = Bounce(); 
Bounce in20 = Bounce(); 
Bounce in21 = Bounce(); 
Bounce in22 = Bounce(); 
Bounce in23 = Bounce(); 
Bounce in24 = Bounce(); 
Bounce in25 = Bounce(); 
Bounce in26 = Bounce(); 
Bounce test=Bounce();
void setup() {
Serial.begin(9600);
  
   Serial.println("Starting ethernet…");
  Ethernet.begin(mac, ip, gateway, gateway, subnet);
  Serial.println(Ethernet.localIP());
  Serial.println("Ready");
  readyState = true;
  myserver.begin();
  
  
  
  
  // Setup the button with an internal pull-up :
  lcd.init();                      // initialize the lcd 
  lcd.init();
  // Print a message to the LCD.
  lcd.backlight();



  
  // After setting up the button, setup the Bounce instance :
  in1.attach(in1Pin,INPUT_PULLUP);
  in1.interval(5); // interval in ms
  in2.attach(in2Pin,INPUT_PULLUP);
  in2.interval(5); // interval in ms
    in3.attach(in3Pin,INPUT_PULLUP);
  in3.interval(5); // interval in ms
    in4.attach(in4Pin,INPUT_PULLUP);
  in4.interval(5); // interval in ms
    in5.attach(in5Pin,INPUT_PULLUP);
  in5.interval(5); // interval in ms
    in6.attach(in6Pin,INPUT_PULLUP);
  in6.interval(5); // interval in ms
    in7.attach(in7Pin,INPUT_PULLUP);
  in7.interval(5); // interval in ms
    in8.attach(in8Pin,INPUT_PULLUP);
  in8.interval(5); // interval in ms
    in9.attach(in9Pin,INPUT_PULLUP);
  in9.interval(5); // interval in ms
    in10.attach(in10Pin,INPUT_PULLUP);
  in10.interval(5); // interval in ms
    in11.attach(in11Pin,INPUT_PULLUP);
  in11.interval(5); // interval in ms
    in12.attach(in12Pin,INPUT_PULLUP);
  in12.interval(5); // interval in ms
    in13.attach(in13Pin,INPUT_PULLUP);
  in13.interval(5); // interval in ms
    in14.attach(in14Pin,INPUT_PULLUP);
  in14.interval(5); // interval in ms
    in15.attach(in15Pin,INPUT_PULLUP);
  in15.interval(5); // interval in ms
    in16.attach(in16Pin,INPUT_PULLUP);
  in16.interval(5); // interval in ms
    in17.attach(in17Pin,INPUT_PULLUP);
  in17.interval(5); // interval in ms
    in18.attach(in18Pin,INPUT_PULLUP);
  in18.interval(5); // interval in ms
    in19.attach(in19Pin,INPUT_PULLUP);
  in19.interval(5); // interval in ms
    in20.attach(in20Pin,INPUT_PULLUP);
  in20.interval(5); // interval in ms
    in21.attach(in21Pin,INPUT_PULLUP);
  in21.interval(5); // interval in ms
    in22.attach(in22Pin,INPUT_PULLUP);
  in22.interval(5); // interval in ms
    in23.attach(in23Pin,INPUT_PULLUP);
  in23.interval(5); // interval in ms
    in24.attach(in24Pin,INPUT_PULLUP);
  in24.interval(5); // interval in ms
    in25.attach(in25Pin,INPUT_PULLUP);
  in25.interval(5); // interval in ms
    in26.attach(in26Pin,INPUT_PULLUP);
  in26.interval(5); // interval in ms
   test.attach(testPin,INPUT_PULLUP);
  test.interval(5); // interval in ms
  //Setup the LED :
  int outputs[24]={14,15,16,17,18,19,23,25,27,29,31,33,35,37,39,41,43,45,47,49,69,68,67,66};
 int  pwm[10]={2,3,4,5,6,7,8,9,11,12};
  lcd.clear();
  Serial.println("TEST MODE");
    lcd.setCursor(0,0);
  lcd.print("TEST MODE");


  for(int i=0;i<10;i++)
  {
pinMode(pwm[i],OUTPUT);
digitalWrite(pwm[i],LOW);
  }

   for(int i=0;i<10;i++)
  {
digitalWrite(pwm[i],HIGH);
delay(500);
  }

  
  for(int j=0;j<24;j++)
  {
    pinMode(outputs[j],OUTPUT);
   digitalWrite(outputs[j],HIGH);
  }
  for(int j=0;j<24;j++)
  {
   delay(500);
      digitalWrite(outputs[j],LOW);

    Serial.println(j);
  }
}

void loop() {
  // Update the Bounce instance :
  in1.update();
  in2.update();
  in3.update();
  in4.update();
  in5.update();
  in6.update();
  in7.update();
  in8.update();
  in9.update();
  in10.update();
  in11.update();
  in12.update();
  in13.update();
  in14.update();
  in15.update();
  in16.update();
  in17.update();
  in18.update();
  in19.update();
  in20.update();
  in21.update();
  in22.update();
  in23.update();
  in24.update();
  in25.update();
  in26.update();
test.update();
if(test.fell())
{
  lcd.clear();
  Serial.println("Houdini");
    lcd.setCursor(0,0);
  lcd.print("Houdini");
  sendHoudini("/clue");

}
if(in1.fell())
{ 
  lcd.clear();
  Serial.println("in1");
    lcd.setCursor(0,0);
  lcd.print("INPUT 1");
}
if(in2.fell())
{
    lcd.clear();
  Serial.println("in2");
    lcd.setCursor(0,0);
  lcd.print("INPUT 2");
}
if(in3.fell())
{
    lcd.clear();

  Serial.println("in3");
   lcd.setCursor(0,0);
  lcd.print("INPUT 3");
}
if(in4.fell())
{
    lcd.clear();

  Serial.println("in4");
   lcd.setCursor(0,0);
  lcd.print("INPUT 4");
}
if(in5.fell())
{
    lcd.clear();

  Serial.println("in5");
   lcd.setCursor(0,0);
  lcd.print("INPUT 5");
}
if(in6.fell())
{
    lcd.clear();

  Serial.println("in6");
   lcd.setCursor(0,0);
  lcd.print("INPUT 6");
}
if(in7.fell())
{
    lcd.clear();

  Serial.println("in7");
   lcd.setCursor(0,0);
  lcd.print("INPUT 7");
}
if(in8.fell())
{
    lcd.clear();

  Serial.println("in8");
   lcd.setCursor(0,0);
  lcd.print("INPUT 8");
}
if(in9.fell())
{
    lcd.clear();

  Serial.println("in9");
   lcd.setCursor(0,0);
  lcd.print("INPUT 9");
}
if(in10.fell())
{
    lcd.clear();

  Serial.println("in10");
   lcd.setCursor(0,0);
  lcd.print("INPUT 10");
}
if(in11.fell())
{
    lcd.clear();

  Serial.println("in11");
   lcd.setCursor(0,0);
  lcd.print("INPUT 11");
}
if(in12.fell())
{
    lcd.clear();

  Serial.println("in12");
   lcd.setCursor(0,0);
  lcd.print("INPUT 12");
}

if(in13.fell())
{
    lcd.clear();

  Serial.println("in13");
   lcd.setCursor(0,0);
  lcd.print("INPUT 13");
}
if(in14.fell())
{
    lcd.clear();

  Serial.println("in14");
   lcd.setCursor(0,0);
  lcd.print("INPUT 14");
}


if(in15.fell())
{
      lcd.clear();

  Serial.println("in15");
   lcd.setCursor(0,0);
  lcd.print("INPUT 15");
}

if(in16.fell())
{
      lcd.clear();

  Serial.println("in16");
   lcd.setCursor(0,0);
  lcd.print("INPUT 16");
}

if(in17.fell())
{
      lcd.clear();

  Serial.println("in17");
   lcd.setCursor(0,0);
  lcd.print("INPUT 17");
}

if(in18.fell())
{
      lcd.clear();

  Serial.println("in18");
   lcd.setCursor(0,0);
  lcd.print("INPUT 18");
}

if(in19.fell())
{
      lcd.clear();

  Serial.println("in19");
   lcd.setCursor(0,0);
  lcd.print("INPUT 19");
}

if(in20.fell())
{
      lcd.clear();

  Serial.println("in20");
   lcd.setCursor(0,0);
  lcd.print("INPUT 20");
}

if(in21.fell())
{
      lcd.clear();

  Serial.println("in21");
   lcd.setCursor(0,0);
  lcd.print("INPUT 21");
}

if(in22.fell())
{
      lcd.clear();

  Serial.println("in22");
   lcd.setCursor(0,0);
  lcd.print("INPUT 22");
}

if(in23.fell())
{
      lcd.clear();

  Serial.println("in23");
   lcd.setCursor(0,0);
  lcd.print("INPUT 23");
}

if(in24.fell())
{
      lcd.clear();

  Serial.println("in24");
   lcd.setCursor(0,0);
  lcd.print("INPUT 24");
}
if(in25.fell())
{
      lcd.clear();

  Serial.println("in25");
   lcd.setCursor(0,0);
  lcd.print("INPUT 25");
}


if(in26.fell())
{
      lcd.clear();

  Serial.println("in26");
   lcd.setCursor(0,0);
  lcd.print("INPUT 26");
}
}


void sendHoudini(const char* URL) {
  String httpStatus = "";
  bool result = true;
  unsigned long tryTIME = millis();
  sprintf(pageAdd, URL);
  while (!getPage(server, serverPort, pageAdd) &&  (millis() - tryTIME <= Timeout) ) {
    result = getPage(server, serverPort, pageAdd);
  }

  if (statusCODE == 200) {
    httpStatus = "Success";
  }
  else if (statusCODE == 404) {
    httpStatus = "NOT FOUND Automation on that URL for Houdini";
  }
  else {
    httpStatus = "UNKNOWN ERROR";
  }

  if (result)
    Serial.println(String(URL) + " -> " + httpStatus);
  else
    Serial.println(String(URL) + " -> Timeout, cannnot connect to HOUDINI");

}

bool getPage(IPAddress ipBuf, int thisPort, char *page)
{
  char outBuf[128];
  String req_str = "";

  Serial.print(F("Connecting…"));
  if (client.connect(ipBuf, thisPort) == 1)
  {
    Serial.println(F("connected"));
    sprintf(outBuf, "GET %s HTTP/1.1", page);
    client.println(outBuf);
    sprintf(outBuf, "Host: %s", serverName);
    client.println(outBuf);
    client.println(F("Connection: close\r\n"));
  }
  else
  {
    Serial.println(F("Failed"));
    return false;
  }

  int connectLoop = 0;
  while (client.connected())
  {
    while (client.available())
    {
      char c = client.read();
      //Serial.write(c);
      req_str += c;
      connectLoop = 0;
    }
    connectLoop++;
    if (connectLoop > 10000)
    {
      Serial.println();
      Serial.println(F("Timeout"));
      client.stop();
    }
    //delay(1);

  }

  Serial.println(F("\r\nDisconnecting."));

  if ( req_str.indexOf("200 OK") != -1 ) {
    statusCODE = 200;
  }
  if ( req_str.indexOf("404") != -1 ) {
    statusCODE = 404;
  }
  if ( statusCODE != 404 && statusCODE != 200 ) {
    statusCODE = 0;
  }

  client.stop();

  return true;
}
