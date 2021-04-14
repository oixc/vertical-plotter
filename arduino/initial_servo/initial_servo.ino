/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

#define SERVO_PIN 12
#define SERVO_POS_UP 100
#define SERVO_POS_DOWN 150 

Servo pen_servo;  // create servo object to control a servo

void setup() {
  pen_servo.attach(SERVO_PIN);  // attaches the servo on pin 9 to the servo object
}

void loop() {
    pen_servo.write(SERVO_POS_UP);
    delay(1000);                 
    pen_servo.write(SERVO_POS_DOWN);
    delay(1000);                
}
