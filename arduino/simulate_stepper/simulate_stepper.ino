/* 
 *  simulate two stepper motors with LEDs blinking for each step & direction
 */
#define MOTOR_LEFT 0
#define MOTOR_RIGHT 1

#define DIRECTION_LEFT 0
#define DIRECTION_RIGHT 1

#define BAUDRATE 9600

int pins[2][2] = {
  {8, 9}, // left
  {11, 12}  // right
};

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(BAUDRATE);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  pinMode(pins[MOTOR_LEFT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_LEFT][DIRECTION_RIGHT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_RIGHT], OUTPUT);

  Serial.println("Ready");  
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
      Serial.print('l');
      break;
    case DIRECTION_RIGHT:
      Serial.print('r');
      break;
  }
  Serial.println();
  blink(pins[motor][dir]); 
}

char c;
String s;

void loop() {
//  blink(pins[MOTOR_LEFT][DIRECTION_LEFT]);
//  blink(pins[MOTOR_LEFT][DIRECTION_RIGHT]);
//  blink(pins[MOTOR_RIGHT][DIRECTION_LEFT]);
//  blink(pins[MOTOR_RIGHT][DIRECTION_RIGHT]);
//  delay(2000);                       

//  rotate(MOTOR_LEFT, DIRECTION_LEFT);
//  rotate(MOTOR_LEFT, DIRECTION_RIGHT);    
//  rotate(MOTOR_RIGHT, DIRECTION_LEFT);
//  rotate(MOTOR_RIGHT, DIRECTION_RIGHT);    
//  delay(1000);     

  while (Serial.available() > 0) {
    //c = Serial.read();
    s = Serial.readStringUntil('\n');
    s.toLowerCase();
    //Serial.println(s);
    if (s == "ll") {
      rotate(MOTOR_LEFT, DIRECTION_LEFT);
    }
    if (s == "lr") {
      rotate(MOTOR_LEFT, DIRECTION_RIGHT);
    }
    if (s == "rl") {
      rotate(MOTOR_RIGHT, DIRECTION_LEFT);
    }
    if (s == "rr") {
      rotate(MOTOR_RIGHT, DIRECTION_RIGHT);
    }
    Serial.flush();
  }
}
