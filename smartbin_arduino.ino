#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial bt (5,6);
Servo Metalservo;
Servo Plasticservo;
Servo Paperservo;
Servo Trashservo;
String btdata;
int pos = 0;

void setup() {
  bt.begin(9600);
  Serial.begin(9600);
  Paperservo.write(pos);      //Sets the initial positions for all the servos
  Metalservo.write(pos);      //Prevents power on jerk 
  Plasticservo.write(pos);
  Trashservo.write(pos);
  Paperservo.attach(11);
  Metalservo.attach(9);
  Plasticservo.attach(10);
  Trashservo.attach(12);
}

void loop() {
  btdata = "";
  delay(100);
 
  if (bt.available()){
    btdata = bt.readString();
    delay(100);
    Serial.println(btdata);

 //Servo operation for Paper recyclable material
 //Servo will open lid for 5 seconds and close after
    if(btdata.equals("Paper") || btdata.equals("Paper product")){
      for(pos=0; pos <=100; pos += 1){
        Paperservo.write(pos);
        delay(15);
      }
      delay(3000);
      for(pos = 100; pos >= 0; pos -= 1){
        Paperservo.write(pos);
        delay(15);
      }
    }

 //Servo operation for Plastic recyclable material
 //Servo will open lid for 5 seconds and close after
   else if(btdata.equals("Plastic") || btdata.equals("Plastic bottle")
            || btdata.equals("Bottle")){
      for(pos=0; pos <=100; pos += 1){
        Plasticservo.write(pos);
        delay(15);
      }
      delay(3000);
      for(pos = 100; pos >= 0; pos -= 1){
        Plasticservo.write(pos);
        delay(15);
      }
    }

 //Servo operation for Metal recyclable material
 //Servo will open lid for 5 seconds and close after
    else if(btdata.equals("Metal") || btdata.equals("Aluminum")
        || btdata.equals("Aluminum can") || btdata.equals("Beverage can")
        || btdata.equals("Tin can")){
      for(pos=0; pos <=100; pos += 1){
        Metalservo.write(pos);
        delay(15);
      }
      delay(3000);
      for(pos = 100; pos >= 0; pos -= 1){
        Metalservo.write(pos);
        delay(15);
      }
    }

  //Default Trash option if no recyclable material was detected 
  //Servo will open lid for 5 seconds and close after
    else{
      for(pos=0; pos <=100; pos += 1){
        Trashservo.write(pos);
        delay(15);
      }
      delay(3000);
      for(pos = 100; pos >= 0; pos -= 1){
        Trashservo.write(pos);
        delay(15);
      }
    }
  }
}
