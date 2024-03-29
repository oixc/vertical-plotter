/* 
 *  main control file for vertical pen plotter
 */
#include <Servo.h>

#define BAUDRATE 9600

#define MOTOR_LEFT 0
#define MOTOR_RIGHT 1

#define DIRECTION_LEFT 0
#define DIRECTION_RIGHT 1

#define DIRECTION_PIN 0
#define STEP_PIN 1

#define PEN_PIN 12
#define PEN_POS_UP 150 // in degree
#define PEN_POS_DOWN 80 // in degree
#define PEN_STEP_SIZE 2 // in degree
#define PEN_DELAY 100 // in ms
#define PEN_STEP_DELAY 10 // in ms

Servo pen_servo;  // create servo object to control the pen lift servo

int pins[2][2] = { // direction, step
  {6, 3}, // left
  {5, 2}  // right
};

int penPin = 4;
int pos = 0;    // variable to store the servo position

int steps_to_home[2] = {0, 0};

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(BAUDRATE);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  pinMode(pins[MOTOR_LEFT][DIRECTION_PIN], OUTPUT);
  pinMode(pins[MOTOR_LEFT][STEP_PIN], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_PIN], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][STEP_PIN], OUTPUT);

  pen_servo.attach(PEN_PIN);
  penUp();

  // Serial.println("Ready");
  //Serial.write('A');
  //Serial.flush();
  establishContact();
}

void setHome() {
  steps_to_home[MOTOR_LEFT] = 0;
  steps_to_home[MOTOR_RIGHT] = 0;
}

void moveHome(int motor) {
  if (steps_to_home[motor] > 0) {
    rotate(motor, DIRECTION_LEFT, steps_to_home[motor]);
  }
  if (steps_to_home[motor] < 0) {
    rotate(motor, DIRECTION_RIGHT, -steps_to_home[motor]);
  }
}
  
void rotate(int motor, int dir, int steps) {
  if (dir == DIRECTION_RIGHT) {
    // Set the spinning direction clockwise:
    digitalWrite(pins[motor][DIRECTION_PIN], HIGH);
    steps_to_home[motor] += steps;
  } else {
    // Set the spinning direction counter clockwise:
    digitalWrite(pins[motor][DIRECTION_PIN], LOW);
    steps_to_home[motor] -= steps;
  }
  for (int i = 0; i < steps; i++) {
    // These four lines result in 1 step:
    digitalWrite(pins[motor][STEP_PIN], HIGH);
    delayMicroseconds(250);
    digitalWrite(pins[motor][STEP_PIN], LOW);
    delayMicroseconds(250);
  }
}

void penDown() {         
  delay(PEN_DELAY);        
  for (pos = PEN_POS_UP; pos >= PEN_POS_DOWN; pos -= PEN_STEP_SIZE) {
    pen_servo.write(pos);              
    delay(PEN_STEP_DELAY );                       
  }
  delay(PEN_DELAY);
}

void penUp() {         
  delay(PEN_DELAY);        
  pen_servo.write(PEN_POS_UP);           
  delay(PEN_DELAY);
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');
    delay(300);
  }  
}

char c;

void loop() {
  if (Serial.available() > 0) {
    c = Serial.read();
    switch (c) {
      case 'a': rotate(MOTOR_LEFT, DIRECTION_LEFT, 1); break;
      case 'b': rotate(MOTOR_LEFT, DIRECTION_RIGHT, 1); break;
      case 'c': rotate(MOTOR_RIGHT, DIRECTION_LEFT, 1); break;
      case 'd': rotate(MOTOR_RIGHT, DIRECTION_RIGHT, 1); break;
      case 'e': penUp(); break;
      case 'f': penDown(); break;
      case 's': setHome(); break;
      case 'h': penUp(); moveHome(MOTOR_RIGHT); moveHome(MOTOR_LEFT); break;
    }
  } else {
    Serial.print('B');
    //delay(1);
    delayMicroseconds(500);
  }
}
