
#include <Wire.h>
#include <Bounce2.h>
#include <Bounce2mcp.h>
#include <Adafruit_MCP23017.h>

#define SCREEN

#ifdef SCREEN
  #include <Adafruit_GFX.h>
  #include <Adafruit_SSD1306.h>
  #define SCREEN_WIDTH 128 // OLED display width, in pixels
  #define SCREEN_HEIGHT 32 // OLED display height, in pixels
  Adafruit_SSD1306 display;
#endif

Adafruit_MCP23017 mcp;

#define BUTTON_PIN1 A0 //IN1
#define BUTTON_PIN2 A1 //IN2
#define BUTTON_PIN3 A2 //IN3
#define BUTTON_PIN4 A3 //IN4

#define BUTTON_PIN5 A6 //RANDOM PIN
#define BUTTON_PIN6 A7 //RANDOM PIN


#define BUTTON_PIN7 6 //IN6
#define BUTTON_PIN8 7 //IN7
#define BUTTON_PIN9 8 //IN8
#define BUTTON_PIN10 9 //IN9
#define BUTTON_PIN11 10 //IN10
#define BUTTON_PIN12 11//IN11

#define atmega1Pin 12
#define testPin 13

Bounce bt1 = Bounce(); // Instantiate a Bounce object
Bounce bt2 = Bounce(); // Instantiate a Bounce object
Bounce bt3 = Bounce(); // Instantiate a Bounce object
Bounce bt4 = Bounce(); // Instantiate a Bounce object
Bounce bt5 = Bounce();
Bounce bt6 = Bounce();
Bounce bt7 = Bounce(); // Instantiate a Bounce object
Bounce bt8 = Bounce(); // Instantiate a Bounce object
Bounce bt9 = Bounce(); // Instantiate a Bounce object
Bounce bt10 = Bounce(); // Instantiate a Bounce object
Bounce bt11 = Bounce();
Bounce bt12 = Bounce();
Bounce atmega1 = Bounce();
Bounce test = Bounce();

BounceMcp mcpin1 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin2 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin3 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin4 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin5 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin6 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin8 = BounceMcp(); // Instantiate a Bounce object

BounceMcp mcpin9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin14 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin15 = BounceMcp(); // Instantiate a Bounce object
BounceMcp mcpin16 = BounceMcp(); // Instantiate a Bounce object

void setup() {
  Serial.begin(9600);
  
  Wire.begin();
  #ifdef SCREEN
    display = Adafruit_SSD1306(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
      Serial.println(F("SSD1306 allocation failed"));
      for (;;);
    }
    delay(500);
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 10);
    display.println("Hello, world!");
    display.display();    
  #endif

  Serial.println("Trying to Setup");
  mcp.begin();
    
  mcp.pinMode(0, INPUT);
  mcp.pullUp(0, HIGH);
  mcp.pinMode(1, INPUT);
  mcp.pullUp(1, HIGH);
  mcp.pinMode(2, INPUT);
  mcp.pullUp(2, HIGH);
  mcp.pinMode(3, INPUT);
  mcp.pullUp(3, HIGH);
  mcp.pinMode(4, INPUT);
  mcp.pullUp(4, HIGH);
  mcp.pinMode(5, INPUT);
  mcp.pullUp(5, HIGH);
  mcp.pinMode(6, INPUT);
  mcp.pullUp(6, HIGH);
  mcp.pinMode(7, INPUT);
  mcp.pullUp(7, HIGH);
  mcp.pinMode(8, INPUT);
  mcp.pullUp(8, HIGH);
  mcp.pinMode(9, INPUT);
  mcp.pullUp(9, HIGH);
  mcp.pinMode(10, INPUT);
  mcp.pullUp(10, HIGH);
  mcp.pinMode(11, INPUT);
  mcp.pullUp(11, HIGH);
  mcp.pinMode(12, INPUT);
  mcp.pullUp(12, HIGH);
  mcp.pinMode(13, INPUT);
  mcp.pullUp(13, HIGH);
  mcp.pinMode(14, INPUT);
  mcp.pullUp(14, HIGH);
  mcp.pinMode(15, INPUT);
  mcp.pullUp(15, HIGH);

  mcpin1.attach(mcp, 0, 25);
  mcpin2.attach(mcp, 1, 25);
  mcpin3.attach(mcp, 2, 25);
  mcpin4.attach(mcp, 3, 25);
  mcpin5.attach(mcp, 4, 25);
  mcpin6.attach(mcp, 5, 25);
  mcpin7.attach(mcp, 6, 25);
  mcpin8.attach(mcp, 7, 25);
  mcpin9.attach(mcp, 8, 25);
  mcpin10.attach(mcp, 9, 25);
  mcpin11.attach(mcp, 10, 25);
  mcpin12.attach(mcp, 11, 25);
  mcpin13.attach(mcp, 12, 25);
  mcpin14.attach(mcp, 13, 25);
  mcpin15.attach(mcp, 14, 25);
  mcpin16.attach(mcp, 15, 25);


  bt1.attach(BUTTON_PIN1, INPUT_PULLUP);
  bt1.interval(25);
  bt2.attach(BUTTON_PIN2, INPUT_PULLUP);
  bt2.interval(25);
  bt3.attach(BUTTON_PIN3, INPUT_PULLUP);
  bt3.interval(25);
  bt4.attach(BUTTON_PIN4, INPUT_PULLUP);
  bt4.interval(25);
  bt5.attach(BUTTON_PIN5, INPUT_PULLUP);
  bt5.interval(25);
  bt6.attach(BUTTON_PIN6, INPUT_PULLUP);
  bt6.interval(25);
  bt7.attach(BUTTON_PIN7, INPUT_PULLUP);
  bt7.interval(25);
  bt8.attach(BUTTON_PIN8, INPUT_PULLUP);
  bt8.interval(25);
  bt9.attach(BUTTON_PIN9, INPUT_PULLUP);
  bt9.interval(25);
  bt10.attach(BUTTON_PIN10, INPUT_PULLUP);
  bt10.interval(25);
  bt11.attach(BUTTON_PIN11, INPUT_PULLUP);
  bt11.interval(25);
  bt12.attach(BUTTON_PIN12, INPUT_PULLUP);
  bt12.interval(25);

  atmega1.attach(atmega1Pin, INPUT_PULLUP);
  atmega1.interval(25);
  test.attach(testPin, INPUT_PULLUP);
  test.interval(25);

  int  pwm[4] = {2, 3, 4, 5};
  for (int i = 0; i < 4; i++)
  {
    pinMode(pwm[i], OUTPUT);
    digitalWrite(pwm[i], LOW);
  }
  for (int i = 0; i < 4; i++)
  {
    digitalWrite(pwm[i], HIGH);
    delay(500);
  }

  Serial.println("Setup completed!");

}

void loop() {

  bt1.update(); // Update the Bounce instance
  bt2.update(); // Update the Bounce instance
  bt3.update(); // Update the Bounce instance
  bt4.update(); // Update the Bounce instance
  bt5.update(); // Update the Bounce instance
  bt6.update(); // Update the Bounce instance
  bt7.update(); // Update the Bounce instance
  bt8.update(); // Update the Bounce instance
  bt9.update(); // Update the Bounce instance
  bt10.update(); // Update the Bounce instance
  bt11.update(); // Update the Bounce instance
  bt12.update(); // Update the Bounce instance
  atmega1.update();
  test.update();

  if (bt1.fell())
  {
    printSL("1");
  }
  if (bt2.fell())
  {

    printSL("2");

  }
  if (bt3.fell())
  {

    printSL("3");

  }
  if (bt4.fell())
  {

    printSL("4");

  }
  if (bt5.fell())
  {

    printSL("5");

  }
  if (bt6.fell())
  {

    printSL("6");

  }
  if (bt7.fell())
  {

    printSL("7");

  }
  if (bt8.fell())
  {

    printSL("8");

  }
  if (bt9.fell())
  {

    printSL("9");

  }
  if (bt10.fell())
  {

    printSL("10");

  }
  if (bt11.fell())
  {

    printSL("11");

  }
  if (bt12.fell())
  {
    
    printSL("12");

  }
  if (atmega1.fell())
  {
    printSL("atmega1");

  }
  if (test.fell())
  {
    printSL("test");
  }


  if (mcpin1.fell())
  {
    printSL("MCPIN1");
  }

  if (mcpin2.fell())
  {
    printSL("MCPIN2");
  }
  if (mcpin3.fell())
  {
    printSL("MCPIN3");
  }
  if (mcpin4.fell())
  {
    printSL("MCPIN4");
  }
  if (mcpin5.fell())
  {
    printSL("MCPIN5");
  }
  if (mcpin6.fell())
  {
    printSL("MCPIN6");
  }
  if (mcpin7.fell())
  {
    printSL("MCPIN7");
  }
  if (mcpin8.fell())
  {
    printSL("MCPIN8");
  }

  if (mcpin9.fell())
  {
    printSL("MCPIN9");
  }
  if (mcpin10.fell())
  {
    printSL("MCPIN10");
  }
  if (mcpin11.fell())
  {
    printSL("MCPIN11");
  }
  if (mcpin12.fell())
  {
    printSL("MCPIN12");
  }
  if (mcpin13.fell())
  {
    printSL("MCPIN13");
  }
  if (mcpin14.fell())
  {
    printSL("MCPIN14");
  }

  if (mcpin15.fell())
  {
    printSL("MCPIN15");
  }
  if (mcpin16.fell())
  {
    printSL("MCPIN16");
  }

}

void printSL ( const char* pr) {

  #ifdef SCREEN
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 10);
    display.println(pr);
    display.display();
  #endif
  Serial.println(pr);
}
