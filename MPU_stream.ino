#include "MPU9250.h"

MPU9250 mpu;


void setup()
{
    Serial.begin(115200);

    Wire.begin();

    mpu.setup();
    Serial.println("Arduino ready");
}

void loop()
{

if (Serial.available()>0)
{
serialFlush();
        mpu.update();
        Serial.print(mpu.getRoll());
        Serial.print(',');
        Serial.print(mpu.getPitch());
        Serial.print(',');
        Serial.println(mpu.getYaw());

 }
 }



    void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}
