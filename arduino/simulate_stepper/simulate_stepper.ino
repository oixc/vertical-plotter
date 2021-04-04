/* 
 *  simulate two stepper motors with LEDs blinking for each step & direction
 */
#define MOTOR_LEFT 0
#define MOTOR_RIGHT 1

#define DIRECTION_LEFT 0
#define DIRECTION_RIGHT 1

int pins[2][2] = {
  {8, 9}, // left
  {11, 12}  // right
};

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  pinMode(pins[MOTOR_LEFT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_LEFT][DIRECTION_RIGHT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_RIGHT], OUTPUT);

  Serial.println('A');  // send READY
}

void blink(int pin) { 
  digitalWrite(pin, HIGH);    
  delay(500);                 
  digitalWrite(pin, LOW);     
}
  
void rotate(int motor, int dir) { 
  switch (motor) {
    case MOTOR_LEFT:
      Serial.print('L');
      break;
    case MOTOR_RIGHT:
      Serial.print('R');
      break;
  }
  switch (dir) {
    case DIRECTION_LEFT:
      Serial.println('l');
      break;
    case DIRECTION_RIGHT:
      Serial.println('r');
      break;
  }
  blink(pins[motor][dir]); 
}

void loop() {
//  blink(pins[MOTOR_LEFT][DIRECTION_LEFT]);
//  blink(pins[MOTOR_LEFT][DIRECTION_RIGHT]);
//  blink(pins[MOTOR_RIGHT][DIRECTION_LEFT]);
//  blink(pins[MOTOR_RIGHT][DIRECTION_RIGHT]);
//  delay(2000);                       
 
  rotate(MOTOR_LEFT, DIRECTION_LEFT);
  rotate(MOTOR_LEFT, DIRECTION_RIGHT);    
  rotate(MOTOR_RIGHT, DIRECTION_LEFT);
  rotate(MOTOR_RIGHT, DIRECTION_RIGHT);    
  delay(1000);     
}
