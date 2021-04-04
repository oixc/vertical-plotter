/* 
 *  simulate two stepper motors with LEDs blinking for each step & direction
 */
#define MOTOR_LEFT 0
#define MOTOR_RIGHT 1

#define DIRECTION_LEFT 0
#define DIRECTION_RIGHT 1

int pins[2][2] = {
  {9, 8}, // left
  {11, 12}  // right
};

void setup() {
  pinMode(pins[MOTOR_LEFT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_LEFT][DIRECTION_RIGHT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_RIGHT], OUTPUT);
}

void blink(int pin) { 
  digitalWrite(pin, HIGH);    
  delay(500);                 
  digitalWrite(pin, LOW);     
}
  
void rotate(int pin) { 
  blink(pin); 
}

void rotateLeft(int motor) { 
  rotate(pins[motor][DIRECTION_LEFT]); 
}

void rotateRight(int motor) { 
  rotate(pins[motor][DIRECTION_RIGHT]); 
}


void loop() {
  blink(pins[MOTOR_LEFT][DIRECTION_LEFT]);
  blink(pins[MOTOR_LEFT][DIRECTION_RIGHT]);
  blink(pins[MOTOR_RIGHT][DIRECTION_LEFT]);
  blink(pins[MOTOR_RIGHT][DIRECTION_RIGHT]);
  delay(2000);                       
}
