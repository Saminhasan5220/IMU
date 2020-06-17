#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET -1
const byte numChars = 32 + 11;
char receivedChars[numChars];

boolean newData = false;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
long   start,last,end;
float frequency  = 0;
void setup() {
    Serial.begin(115200);
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    display.clearDisplay();
    display.setTextColor(WHITE);
    display.setCursor(0,0);
    display.println("Arduino initialized");
    display.println("Standing by");

    display.display();
       display.clearDisplay();
    display.setTextColor(WHITE);
    display.setCursor(0,0);
    display.println("Standby");
    display.display();
    Serial.println("Arduino initialized");
    Serial.println("Standby");

    start = millis();
}

void loop() {

end = millis();
if ((end - start)!=0)
frequency = 1000/(float)(end - start);
recvWithEndMarker();
if (newData || (end - last)> 50){
display.clearDisplay();
display.setTextColor(WHITE);
display.setCursor(0,0);
display.print(frequency);
display.println(" Hz");
showNewData();
display.display();
last = millis();
}
start = end;
}
/*
shape = (4,21) # char size 1 
shape = (1,4) # char size 4 

*/
void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
   
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}


void showNewData() {
    if (newData == true) {
        display.println("Incoming message:");
        display.println(receivedChars);
        Serial.print("Incoming message:");
        Serial.println(receivedChars);
        newData = false;
    }
    else
    {
        display.println("Incoming message:");
        display.println(receivedChars);
      }
}
