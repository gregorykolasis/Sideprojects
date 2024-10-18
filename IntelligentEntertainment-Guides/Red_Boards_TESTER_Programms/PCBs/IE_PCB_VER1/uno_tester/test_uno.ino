#include <Bounce2.h>
#include <Wire.h>
#include <Bounce2mcp.h>
#include <Adafruit_MCP23017.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

int digits = 4;
char pass[4] = {'0', '*', '*', '7'};
char fillpass[4];
int succeed;
int i = 0;
int j = 0;
int period = 20000;
unsigned long timenow = 0;

Adafruit_MCP23017 mcp;

#define BUTTON_PIN1 A0 //IN1
#define BUTTON_PIN2 A1 //IN2
#define BUTTON_PIN3 A2 //IN3
#define BUTTON_PIN4 A3 //IN4
#define BUTTON_PIN5 2 //IN4
#define BUTTON_PIN6 4 //IN4

#define mega1Pin 7
#define mega2Pin 8

Bounce bt1 = Bounce(); // Instantiate a Bounce object
Bounce bt2 = Bounce(); // Instantiate a Bounce object
Bounce bt3 = Bounce(); // Instantiate a Bounce object
Bounce bt4 = Bounce(); // Instantiate a Bounce object
Bounce bt5 = Bounce();
Bounce bt6 = Bounce();

BounceMcp bt7 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt8 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt9 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt10 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt11 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt12 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt13 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt14 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt15 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt16 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt17 = BounceMcp(); // Instantiate a Bounce object
BounceMcp bt18 = BounceMcp(); // Instantiate a Bounce object

Bounce mega1 = Bounce(); // Instantiate a Bounce object
Bounce mega2 = Bounce(); // Instantiate a Bounce object

char customkey;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  lcd.init();                      // initialize the lcd 
  lcd.init();
  // Print a message to the LCD.
  lcd.backlight();
    lcd.clear();
  Serial.println("TEST MODE");
    lcd.setCursor(0,0);
  lcd.print("TEST MODE");
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

  mega1.attach(mega1Pin, INPUT_PULLUP);
  mega1.interval(25);

  mega2.attach(mega2Pin, INPUT_PULLUP);
  mega2.interval(25);
  
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
  
  bt7.attach(mcp,0,25);  
  bt8.attach(mcp,1,25);  
  bt9.attach(mcp,2,25);  
  bt10.attach(mcp,3,25);  
  bt11.attach(mcp,4,25);  
  bt12.attach(mcp,5,25);  
  bt13.attach(mcp,8,25);  
  bt14.attach(mcp,9,25);  
  bt15.attach(mcp,10,25);  
  bt16.attach(mcp,11,25);  
  bt17.attach(mcp,12,25);  
  bt18.attach(mcp,13,25);  
 int  pwm[4]={3,5,6,9};
  for(int i=0;i<4;i++)
  {
pinMode(pwm[i],OUTPUT);
digitalWrite(pwm[i],LOW);
  }
   for(int i=0;i<4;i++)
  {
digitalWrite(pwm[i],HIGH);
delay(500);
  }
  

}

void loop() {
  // put your main code here, to run repeatedly:
  bt1.update(); // Update the Bounce instance
  bt2.update(); // Update the Bounce instance
  bt3.update(); // Update the Bounce instance
  bt4.update(); // Update the Bounce instance
  bt5.update(); // Update the Bounce instance
  bt6.update(); // Update the Bounce instance
  mega1.update(); // Update the Bounce instance
  mega2.update(); // Update the Bounce instance

if(bt1.fell())
{
  Serial.println("1");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("1");
}
if(bt2.fell())
{
  Serial.println("2");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("2");
}
if(bt3.fell())
{
  Serial.println("3");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("3");
}
if(bt4.fell())
{
  Serial.println("4");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("4");
}
if(bt5.fell())
{
  Serial.println("5");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("5");
}
if(bt6.fell())
{
  Serial.println("6");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("6");
}
if(bt7.fell())
{
  Serial.println("7");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("7");
}
if(bt8.fell())
{
  Serial.println("8");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("8");
}
if(bt9.fell())
{
  Serial.println("9");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("9");
}
if(bt10.fell())
{
  Serial.println("10");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("10");
}
if(bt11.fell())
{
  Serial.println("11");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("11");
}
if(bt12.fell())
{
  Serial.println("12");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("12");
}
if(bt13.fell())
{
  Serial.println("13");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("13");
}
if(bt14.fell())
{
  Serial.println("14");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("14");
}

if(bt15.fell())
{
  Serial.println("15");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("15");
}
if(bt16.fell())
{
  Serial.println("16");
    lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("16");
}
if(bt17.fell())
{
  Serial.println("17");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("17");
}
if(bt18.fell())
{
  Serial.println("18");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("18");
}
if(mega1.fell())
{
  Serial.println("mega1");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("mega1");
}
if(mega2.fell())
{
  Serial.println("mega2");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("mega2");
}








}
