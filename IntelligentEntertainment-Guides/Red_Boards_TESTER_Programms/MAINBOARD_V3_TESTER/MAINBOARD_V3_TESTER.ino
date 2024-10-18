/* 
 DESCRIPTION
 ====================
 Simple example of the Bounce library that switches the debug LED when a button is pressed.
 */
// Include the Bounce2 library found here :
// https://github.com/thomasfredericks/Bounce2
#include <Bounce2.h>
#include <Wire.h> 
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MCP23017.h>
#include <Bounce2mcp.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

Adafruit_MCP23017 mcp1;
Adafruit_MCP23017 mcp2;
Adafruit_MCP23017 mcp3;
Adafruit_MCP23017 mcp4;
Adafruit_MCP23017 mcp5;
Adafruit_MCP23017 mcp6;
Adafruit_MCP23017 mcp7;

#define addr1 0
#define addr2 4
#define addr3 2
#define addr4 1
#define addr5 5
#define addr6 6
#define addr7 7

#define in1Pin 40
#define in2Pin 41
#define in3Pin 42 
#define in4Pin 43
#define in5Pin 44
#define in6Pin 45
#define in7Pin 46
#define in8Pin 47
#define in9Pin 48
#define in10Pin 49
#define in11Pin 69
#define in12Pin 68
#define in13Pin 67
#define in14Pin 66
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
int mcpButtons[]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
 int  pwm[10]={2,3,4,5,6,7,8,9,11,12};

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

BounceMcp mcp1in1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in6 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in8 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp1in14 = BounceMcp(); // Instantiate a Bounce object



BounceMcp mcp2in1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in6 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in8 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp2in14 = BounceMcp(); // Instantiate a Bounce object


BounceMcp mcp3in1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in6 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in8 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp3in14 = BounceMcp(); // Instantiate a Bounce object

BounceMcp mcp4in1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp4in2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp4in3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp4in4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp4in5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp4in6 = BounceMcp(); // Instantiate a Bounce object

BounceMcp mcp5in1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in6 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in8 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in14 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in15 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp5in16 = BounceMcp(); // Instantiate a Bounce object

BounceMcp mcp6in1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in6 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in8 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in14 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in15 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp6in16 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in6 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in8 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in14 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in15 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcp7in16 = BounceMcp(); // Instantiate a Bounce object1
void setup() {

Serial.begin(9600);

Serial.println("preInit");

mcp1.begin();
mcp2.begin(addr2); 
mcp3.begin(addr3);
mcp4.begin(addr4);
mcp5.begin(addr5);
mcp6.begin(addr6);
mcp7.begin(addr7);

Serial.println("MPCS Begun!");

for(int i=0;i<14;i++)
{
mcp1.pinMode(i,INPUT);
mcp1.pullUp(i,HIGH);

}

mcp1in1.attach(mcp1, 0, 25);
mcp1in2.attach(mcp1, 1, 25);
mcp1in3.attach(mcp1, 2, 25);
mcp1in4.attach(mcp1, 3, 25);
mcp1in5.attach(mcp1, 4, 25);
mcp1in6.attach(mcp1, 5, 25);
mcp1in7.attach(mcp1, 6, 25);
mcp1in8.attach(mcp1, 7, 25);
mcp1in9.attach(mcp1, 8, 25);
mcp1in10.attach(mcp1, 9, 25);
mcp1in11.attach(mcp1, 10, 25);
mcp1in12.attach(mcp1, 11, 25);
mcp1in13.attach(mcp1, 12, 25);
mcp1in14.attach(mcp1, 13, 25);


for(int i=0;i<14;i++)
{
mcp2.pinMode(i,INPUT);
mcp2.pullUp(i,HIGH);

}

mcp2in1.attach(mcp2, 0, 25);
mcp2in2.attach(mcp2, 1, 25);
mcp2in3.attach(mcp2, 2, 25);
mcp2in4.attach(mcp2, 3, 25);
mcp2in5.attach(mcp2, 4, 25);
mcp2in6.attach(mcp2, 5, 25);
mcp2in7.attach(mcp2, 6, 25);
mcp2in8.attach(mcp2, 7, 25);
mcp2in9.attach(mcp2, 8, 25);
mcp2in10.attach(mcp2, 9, 25);
mcp2in11.attach(mcp2, 10, 25);
mcp2in12.attach(mcp2, 11, 25);
mcp2in13.attach(mcp2, 12, 25);
mcp2in14.attach(mcp2, 13, 25);



for(int i=0;i<14;i++)
{
mcp3.pinMode(i,INPUT);
mcp3.pullUp(i,HIGH);

}
 
mcp3in1.attach(mcp3, 0, 25);
mcp3in2.attach(mcp3, 1, 25);
mcp3in3.attach(mcp3, 2, 25);
mcp3in4.attach(mcp3, 3, 25);
mcp3in5.attach(mcp3, 4, 25);
mcp3in6.attach(mcp3, 5, 25);
mcp3in7.attach(mcp3, 6, 25);
mcp3in8.attach(mcp3, 7, 25);
mcp3in9.attach(mcp3, 8, 25);
mcp3in10.attach(mcp3, 9, 25);
mcp3in11.attach(mcp3, 10, 25);
mcp3in12.attach(mcp3, 11, 25);
mcp3in13.attach(mcp3, 12, 25);
mcp3in14.attach(mcp3, 13, 25);

for(int i=8;i<14;i++)
{
mcp4.pinMode(i,INPUT);
mcp4.pullUp(i,HIGH);

}

mcp4in1.attach(mcp4, 8, 25);
mcp4in2.attach(mcp4, 9, 25);
mcp4in3.attach(mcp4, 10, 25);
mcp4in4.attach(mcp4, 11, 25);
mcp4in5.attach(mcp4, 12, 25);
mcp4in6.attach(mcp4, 13, 25);


for(int i=0;i<16;i++)
{
mcp5.pinMode(i,INPUT);
mcp5.pullUp(i,HIGH);

}
 
mcp5in1.attach(mcp5, 0, 25);
mcp5in2.attach(mcp5, 1, 25);
mcp5in3.attach(mcp5, 2, 25);
mcp5in4.attach(mcp5, 3, 25);
mcp5in5.attach(mcp5, 4, 25);
mcp5in6.attach(mcp5, 5, 25);
mcp5in7.attach(mcp5, 6, 25);
mcp5in8.attach(mcp5, 7, 25);
mcp5in9.attach(mcp5, 8, 25);
mcp5in10.attach(mcp5, 9, 25);
mcp5in11.attach(mcp5, 10, 25);
mcp5in12.attach(mcp5, 11, 25);
mcp5in13.attach(mcp5, 12, 25);
mcp5in14.attach(mcp5, 13, 25);
mcp5in15.attach(mcp5, 14, 25);
mcp5in16.attach(mcp5, 15, 25);

for(int i=0;i<16;i++)
{
mcp6.pinMode(i,INPUT);
mcp6.pullUp(i,HIGH);

}
 
mcp6in1.attach(mcp6, 0, 25);
mcp6in2.attach(mcp6, 1, 25);
mcp6in3.attach(mcp6, 2, 25);
mcp6in4.attach(mcp6, 3, 25);
mcp6in5.attach(mcp6, 4, 25);
mcp6in6.attach(mcp6, 5, 25);
mcp6in7.attach(mcp6, 6, 25);
mcp6in8.attach(mcp6, 7, 25);
mcp6in9.attach(mcp6, 8, 25);
mcp6in10.attach(mcp6, 9, 25);
mcp6in11.attach(mcp6, 10, 25);
mcp6in12.attach(mcp6, 11, 25);
mcp6in13.attach(mcp6, 12, 25);
mcp6in14.attach(mcp6, 13, 25);
mcp6in15.attach(mcp6, 14, 25);
mcp6in16.attach(mcp6, 15, 25);

for(int i=0;i<16;i++)
{
mcp7.pinMode(i,INPUT);
mcp7.pullUp(i,HIGH);

}
 
mcp7in1.attach(mcp7, 0, 25);
mcp7in2.attach(mcp7, 1, 25);
mcp7in3.attach(mcp7, 2, 25);
mcp7in4.attach(mcp7, 3, 25);
mcp7in5.attach(mcp7, 4, 25);
mcp7in6.attach(mcp7, 5, 25);
mcp7in7.attach(mcp7, 6, 25);
mcp7in8.attach(mcp7, 7, 25);
mcp7in9.attach(mcp7, 8, 25);
mcp7in10.attach(mcp7, 9, 25);
mcp7in11.attach(mcp7, 10, 25);
mcp7in12.attach(mcp7, 11, 25);
mcp7in13.attach(mcp7, 12, 25);
mcp7in14.attach(mcp7, 13, 25);
mcp7in15.attach(mcp7, 14, 25);
mcp7in16.attach(mcp7, 15, 25);


mcp1.pinMode(14,OUTPUT);
mcp1.pinMode(15,OUTPUT);
mcp2.pinMode(14,OUTPUT);
mcp2.pinMode(15,OUTPUT);
mcp3.pinMode(14,OUTPUT);
mcp3.pinMode(15,OUTPUT);
mcp4.pinMode(0,OUTPUT);
mcp4.pinMode(1,OUTPUT);
mcp4.pinMode(2,OUTPUT);
mcp4.pinMode(3,OUTPUT);
mcp4.pinMode(4,OUTPUT);
mcp4.pinMode(5,OUTPUT);
mcp4.pinMode(6,OUTPUT);
mcp4.pinMode(7,OUTPUT);
mcp4.pinMode(14,OUTPUT);
mcp4.pinMode(15,OUTPUT);

mcp1.digitalWrite(14,LOW);
mcp1.digitalWrite(15,LOW);
mcp2.digitalWrite(14,LOW); 
mcp2.digitalWrite(15,LOW); 
mcp3.digitalWrite(14,LOW);
mcp3.digitalWrite(15,LOW); 
mcp4.digitalWrite(0,LOW); 
mcp4.digitalWrite(1,LOW); 
mcp4.digitalWrite(2,LOW); 
mcp4.digitalWrite(3,LOW); 
mcp4.digitalWrite(4,LOW); 
mcp4.digitalWrite(5,LOW); 
mcp4.digitalWrite(6,LOW); 
mcp4.digitalWrite(7,LOW);
mcp4.digitalWrite(14,LOW); 
mcp4.digitalWrite(15,LOW); 



  
 if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
  }
  delay(2000);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(20, 30);
  // Display static text
  display.println("Hello, world!");
  display.display(); 
  
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
  int outputs[24]={14,15,16,17,18,19,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39};


  for(int i=0;i<10;i++)
  {
    pinMode(pwm[i],OUTPUT);
    digitalWrite(pwm[i],LOW);
  }
  for(int i=0;i<10;i++)
  {
    
    //if (i==6) continue;
    //if (i==7) continue;
    //if (i==8) continue;
    
    digitalWrite(pwm[i],HIGH);
    delay(500);
    Serial.println("[Opening-PWM] "+String(i+1));
  }
  
  mcp1.digitalWrite(14,HIGH); delay(500);
  mcp1.digitalWrite(15,HIGH); delay(500);
  
  mcp2.digitalWrite(14,HIGH); delay(500);
  mcp2.digitalWrite(15,HIGH); delay(500);
  
  mcp3.digitalWrite(14,HIGH); delay(500);
  mcp3.digitalWrite(15,HIGH); delay(500);
  mcp4.digitalWrite(0,HIGH); delay(500);
  mcp4.digitalWrite(1,HIGH); delay(500);
  mcp4.digitalWrite(2,HIGH); delay(500);
  mcp4.digitalWrite(3,HIGH); delay(500);
  mcp4.digitalWrite(4,HIGH); delay(500);
  mcp4.digitalWrite(5,HIGH); delay(500);
  mcp4.digitalWrite(6,HIGH); delay(500);
  mcp4.digitalWrite(7,HIGH); delay(500);
  mcp4.digitalWrite(14,HIGH); delay(500);
  mcp4.digitalWrite(15,HIGH); delay(500);


  for(int j=0;j<24;j++)
  {
    pinMode(outputs[j],OUTPUT);
    digitalWrite(outputs[j],LOW);
    delay(500);
    Serial.println("[Opening-REL]"+String(j+1));
  }

  Serial.println("Everything OK");
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
 printSL("TEST");
}
if(in1.fell())
{ 
  printSL("in1");

}
if(in2.fell())
{
   printSL("in2");

}
if(in3.fell())
{
   printSL("in3");

}
if(in4.fell())
{
  printSL("in4");

}
if(in5.fell())
{
 printSL("in5");

}
if(in6.fell())
{
   printSL("in6");

}
if(in7.fell())
{
  printSL("in7");


}
if(in8.fell())
{
 printSL("in8");

  
}
if(in9.fell())
{
 printSL("in9");
}
if(in10.fell())
{
    printSL("in10");
  
}
if(in11.fell())
{
 printSL("in11");
}
if(in12.fell())
{
 printSL("in12");

}

if(in13.fell())
{
 printSL("in13");


}
if(in14.fell())
{
 printSL("in14");  
}


if(in15.fell())
{
 printSL("in15");

}

if(in16.fell())
{
 printSL("in16");

}

if(in17.fell())
{
 printSL("in17");

}

if(in18.fell())
{
 printSL("in18");

}

if(in19.fell())
{
 printSL("in19");

}

if(in20.fell())
{
 printSL("in20");

}

if(in21.fell())
{
 printSL("in21");

}

if(in22.fell())
{
  printSL("in22");

}

if(in23.fell())
{
 printSL("in23");

}

if(in24.fell())
{
  printSL("in24");

}
if(in25.fell())
{
  printSL("in25");

}


if(in26.fell())
{
  printSL("in26");
}
if(mcp1in1.fell())
{
  printSL("mcp1in1");

}
if(mcp1in2.fell())
{
   printSL("mc1in2");

}

if(mcp1in3.fell())
{
   printSL("mc1in3");

}

if(mcp1in4.fell())
{
    printSL("mc1in4");

}

if(mcp1in5.fell())
{
   printSL("mc1in5");

}
if(mcp1in6.fell())
{
   printSL("mc1in6");

}


if(mcp1in7.fell())
{
   printSL("mc1in7");

}

if(mcp1in8.fell())
{
   printSL("mc1in8");

}

if(mcp1in9.fell())
{
  printSL("mc1in9");

}
if(mcp1in10.fell())
{
    printSL("mc1in10");

}

if(mcp1in11.fell())
{
   printSL("mc1in11");

}

if(mcp1in12.fell())
{
   printSL("mc1in12");

}

if(mcp1in13.fell())
{
   printSL("mc1in13");

}
if(mcp1in14.fell())
{
   printSL("mc1in14");

}




if(mcp2in1.fell())
{
   printSL("mc2in1");

}
if(mcp2in2.fell())
{
     printSL("mc2in2");

}

if(mcp2in3.fell())
{
    printSL("mc2in3");

}

if(mcp2in4.fell())
{
    printSL("mc2in4");

}

if(mcp2in5.fell())
{
    printSL("mc2in5");

}
if(mcp2in6.fell())
{
   printSL("mc2in6");

}


if(mcp2in7.fell())
{
    printSL("mc2in7");

}

if(mcp2in8.fell())
{
    printSL("mc2in8");

}

if(mcp2in9.fell())
{
   printSL("mc2in9");

}
if(mcp2in10.fell())
{
     printSL("mc2in10");

}

if(mcp2in11.fell())
{
    printSL("mc2in11");

}

if(mcp2in12.fell())
{
    printSL("mc2in12");

}

if(mcp2in13.fell())
{
    printSL("mc2in13");

}
if(mcp2in14.fell())
{
   printSL("mc2in14");

}







if(mcp3in1.fell())
{
    printSL("mc3in1");

}
if(mcp3in2.fell())
{
    printSL("mc3in2");

}

if(mcp3in3.fell())
{
    printSL("mc3in3");

}

if(mcp3in4.fell())
{
     printSL("mc3in4");

}

if(mcp3in5.fell())
{
    printSL("mc3in5");

}
if(mcp3in6.fell())
{
  printSL("mc3in6");
}


if(mcp3in7.fell())
{
 printSL("mc3in7");
}

if(mcp3in8.fell())
{
     printSL("mc3in8");

}

if(mcp3in9.fell())
{
    printSL("mc3in9");

}
if(mcp3in10.fell())
{
    printSL("mc3in10");

}

if(mcp3in11.fell())
{
    printSL("mc3in11");

}

if(mcp3in12.fell())
{
     printSL("mc3in12");

}

if(mcp3in13.fell())
{
    printSL("mc3in13");

}
if(mcp3in14.fell())
{
  printSL("mc3in14");
}

if(mcp4in1.fell())
{
  printSL("mc4in1");
}


if(mcp4in2.fell())
{
  printSL("mc4in2");
}


if(mcp4in3.fell())
{
  printSL("mc4in3");
}


if(mcp4in4.fell())
{
  printSL("mc4in4");
}


if(mcp4in5.fell())
{
  printSL("mc4in5");
}


if(mcp4in6.fell())
{
  printSL("mc4in6");
}


if(mcp5in1.fell())
{
  printSL("mc5in1");
}

if(mcp5in2.fell())
{
  printSL("mc5in2");
}

if(mcp5in3.fell())
{
  printSL("mc5in3");
}

if(mcp5in4.fell())
{
  printSL("mc5in4");
}


if(mcp5in5.fell())
{
  printSL("mc5in5");
}


if(mcp5in6.fell())
{
  printSL("mc5in6");
}


if(mcp5in7.fell())
{
  printSL("mc5in7");
}


if(mcp5in8.fell())
{
  printSL("mc5in8");
}


if(mcp5in9.fell())
{
  printSL("mc5in9");
}

if(mcp5in10.fell())
{
  printSL("mc5in10");
}

if(mcp5in11.fell())
{
  printSL("mc5in11");
}


if(mcp5in12.fell())
{
  printSL("mc5in12");
}

if(mcp5in13.fell())
{
  printSL("mc5in13");
}

if(mcp5in14.fell())
{
  printSL("mc5in14");
}
if(mcp5in15.fell())
{
  printSL("mc5in15");
}
if(mcp5in16.fell())
{
  printSL("mc5in16");
}

if(mcp6in1.fell())
{
  printSL("mc6in1");
}

if(mcp6in2.fell())
{
  printSL("mc6in2");
}

if(mcp6in3.fell())
{
  printSL("mc6in3");
}

if(mcp6in4.fell())
{
  printSL("mc6in4");
}


if(mcp6in5.fell())
{
  printSL("mc6in5");
}


if(mcp6in6.fell())
{
  printSL("mc6in6");
}


if(mcp6in7.fell())
{
  printSL("mc6in7");
}


if(mcp6in8.fell())
{
  printSL("mc6in8");
}


if(mcp6in9.fell())
{
  printSL("mc6in9");
}

if(mcp6in10.fell())
{
  printSL("mc6in10");
}

if(mcp6in11.fell())
{
  printSL("mc6in11");
}


if(mcp6in12.fell())
{
  printSL("mc6in12");
}

if(mcp6in13.fell())
{
  printSL("mc6in13");
}

if(mcp6in14.fell())
{
  printSL("mc6in14");
}
if(mcp6in15.fell())
{
  printSL("mc6in15");
}
if(mcp6in16.fell())
{
  printSL("mc6in16");
}

if(mcp7in1.fell())
{
  printSL("mc7in1");
}

if(mcp7in2.fell())
{
  printSL("mc7in2");
}

if(mcp7in3.fell())
{
  printSL("mc7in3");
}

if(mcp7in4.fell())
{
  printSL("mc7in4");
}


if(mcp7in5.fell())
{
  printSL("mc7in5");
}


if(mcp7in6.fell())
{
  printSL("mc7in6");
}


if(mcp7in7.fell())
{
  printSL("mc7in7");
}


if(mcp7in8.fell())
{
  printSL("mc7in8");
}


if(mcp7in9.fell())
{
  printSL("mc7in9");
}

if(mcp7in10.fell())
{
  printSL("mc7in10");
}

if(mcp7in11.fell())
{
  printSL("mc7in11");
}


if(mcp7in12.fell())
{
  printSL("mc7in12");
}

if(mcp7in13.fell())
{
  printSL("mc7in13");
}

if(mcp7in14.fell())
{
  printSL("mc7in14");
}
if(mcp7in15.fell())
{
  printSL("mc7in15");
}
if(mcp7in16.fell())
{
  printSL("mc7in16");
}




}



void printSL ( const char* pr) {
  display.clearDisplay();
  Serial.println(pr);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  display.println(pr);
  display.display(); 
} 
